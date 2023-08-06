from os.path import split, splitext, isfile, exists, join, isdir, abspath
from os import listdir, makedirs, mkdir, remove, rmdir
from .Children import Children
from .Abstrcat import Abstract
from .btype import FILE, DIR
import shutil


class Block:

    def __init__(self, path: str) -> None:
        '''
            @parameter path - 文件/文件夹路径
        '''
        self.__path = path
    
    def enter(self, path):
        self.__path = self.join_path(path)
    
    @property
    def path(self):
        return self.__path
    
    @property
    def abspath(self):
        return abspath(self.path)
    
    @property
    def directory(self):
        return split(self.path)[0]
    
    @property
    def file_full_name(self):
        return split(self.path)[1]
    
    @property
    def filename(self):
        return splitext(self.file_full_name)[0]
    
    @property
    def extension(self):
        return splitext(self.file_full_name)[1]
    
    def sub_block(self, path: str):
        '''
            @parameter path - 子文件或子文件夹的相对路径
            @returns
                子文件/子文件夹的Block对象
        '''
        sub_path = self.join_path(path)
        return Block(sub_path)
    
    def append(self, name, type=FILE):
        '''
            往block中新增一个文件/文件夹

            TIPS:
                当type == FILE时，若name形如x1/x2, 则会新建x1文件夹，返回的是x2的Block对象，而不是x1
        '''
        path = self.join_path(name)
        if type == FILE:
            dir_name, _ = split(path)
            if not exists(dir_name):
                makedirs(dir_name)
            with open(path, 'w+') as f:
                pass
        elif type == DIR:
            makedirs(path)
        return Block(path)

    def join_path(self, path: str)->str:
        '''
            @parameter path - 需要拼接的文件/文件夹路径
            @returns:
                拼接后的路径
        '''
        return join(self.path, path)
    
    def remove(self):
        '''
             如果该block对象是真实存在的文件/文件夹, 则从磁盘上永久删除该文件/文件夹
        '''
        if self.exists:
            if self.isfile:
                remove(self.path)
            else:
                rmdir(self.path)
        else:
            raise FileNotFoundError("文件/文件夹不存在时，无法执行block.remove()")

    def moveTo(self, target):
        if type(target) == str:
            target = Block(target)
        if not self.exists:
            raise FileNotFoundError(self.path, " not found! ")
        if not target.exists:
            makedirs(target.path)
        if not target.isdir:
            raise Exception(target.path, " is not a dir.")
        shutil.move(self.path, target.path)
        return self
        
    def copyTo(self, target):
        if type(target) == str:
            target = Block(target)
        if not self.exists:
            raise FileNotFoundError(self.path, " not found! ")
        if not target.exists:
            makedirs(target.path)
        if not target.isdir:
            raise Exception(target.path, " is not a dir.")
        mask_len = len(self.abspath)
        if self.isfile:
            path = target.join_path(self.file_full_name)
            with open(path, 'wb+') as f:
                f.write(self.get_file_contents())
        else:
            for leaf in self.leaves:
                path = target.join_path("." + leaf.abspath[mask_len:])
                dir_path, name = split(path)
                if leaf.isfile:
                    if not exists(dir_path):
                        makedirs(dir_path)
                    with open(path, 'wb+') as f:
                        f.write(leaf.get_file_contents())
                else:
                    if not exists(path):
                        makedirs(path)
        return self

    def search(self, name, type=None)->Children:
        '''
            在block内进行搜索，返回所有匹配的文件/文件夹
            
            可选参数type的值应为 fileblock.FILE 或 fileblock.DIR
        '''
        leaves = self.leaves
        return [
            leaf for leaf in leaves
            if name in split(leaf.path)[1] and ((type is not None and leaf.btype==type) or type is None)
        ]
    
    @property
    def leaves(self) -> Children:
        '''
        返回文件树中的所有叶子节点
        '''
        children = self.children
        if len(children) > 0:
            res = Children()
            for child in children:
                res.extend(child.leaves)
            return res
        else:
            return Children([self])

    def cut(self, *rates):
        '''
            切割文件夹内的文件块
            @parameter - rates 分割比例，可以是整数，也可以是浮点数
        '''
        if not rates:
            rates = (1, )
        if not self.isdir:
            return None
        children = self.children
        gross = sum(rates)
        n = children.__len__()
        cell = n / gross
        acc = 0
        res = []
        rates_len = len(rates)
        for i in range(len(rates)):
            if rates_len == i + 1:
                res.append(children[acc : ])
            else:
                idx = int(rates[i] * cell)
                res.append(children[acc : acc + idx])
                acc += idx
        return res
    
    def get_file_contents(self):
        if self.isfile:
            with open(self.path, 'rb') as f:
                d = f.read()
            return d
        raise TypeError("This block is not a file-type block")

    @property
    def isfile(self) -> bool:
        '''
            block类型是文件则返回True
        '''
        return isfile(self.path)

    @property
    def isdir(self) -> bool:
        '''
            block类型是文件夹则返回True
        '''
        return isdir(self.path)
    
    @property
    def exists(self) -> bool:
        '''
            该block是否存在
        '''
        return exists(self.path)
    
    @property
    def children(self) -> Children:
        res = Children()
        if self.isdir:
            dirs = listdir(self.path)
            for dir in dirs:
                res.append(self.sub_block(dir))
        return res

    
    @property
    def btype(self):
        return FILE if self.isfile else DIR if self.isdir else None
    
    def abstract(self, force_abspath=False):
        return Abstract(self.btype, self.abspath if force_abspath else self.path)

    def __str__(self):
        # return "(%s block: %s)" % (self.btype, self.path)
        return self.path
    
    def __repr__(self) -> str:
        return self.__str__()

    @property
    def super_dir_name(self):
        tmp = split(self.path)[0]
        return split(tmp)[1]



if __name__ == "__main__":

    b = Block("../")
    print(b.children)