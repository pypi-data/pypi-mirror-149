from random import random
import json
from .btype import __BaseType__

class Children:

    def __init__(self, data=[], copy=True):
        if isinstance(data, Children):
            data = data.data
        if copy:
            self.data = data.copy()
        else:
            self.data = data


    def map(self, fn):
        def dfs(x):
            return Children([
                dfs(cell) if hasattr(cell, "__iter__") else fn(cell)
                for cell in x
            ])
        return dfs(self)
        

    def to_json(self, fpath: str, file_only=False, dir_only=False, abspath = False, indent=None, encoding="utf8"):
        """注：若file_only 和 dir_only 同时为 True 则 全都输出."""
        def convert(child):
            if type(child) == Children:
                res = []
                for c in child:
                    tmp = convert(c)
                    if tmp:
                        res.append(tmp)
                return res
            if file_only and not dir_only:
                if child.isfile:
                    return child.abstract(abspath).__dict__
            elif dir_only and not file_only:
                if child.isdir:
                    return child.abstract(abspath).__dict__
            else:
                return child.abstract(abspath).__dict__

        data = convert(self)
        with open(fpath, "w+", encoding=encoding) as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        

    def unfold(self):
        def proc(children):
            if type(children[0]) == Children:
                tmp = Children()
                for child in children:
                    tmp += proc(child)
                return tmp
            return children
        res = proc(self)
        return res


    def copy(self):
        return Children(self.data, copy=True)


    def shuffle(self):
        res = self.copy()
        le = res.__len__()
        for i in range(1, le+1):
            idx = int(random() * (le - i))
            res[idx], res[le - i] = res[le - i], res[idx]
        return res
    

    def append(self, obj):
        self.data.append(obj)
        return self


    def extend(self, obj):
        self.data.extend(obj)
        return self
    

    def remove(self, x):
        self.data.remove(x)
        return self


    def pop(self, *idx):
        # TODO: 应该从后往前pop，保持pop的正确性
        res = []
        def dfs(idx):
            if hasattr(idx, "__iter__"):
                for i in idx:
                    dfs(i)
            else:
                res.append(self.data.pop(idx))
        dfs(idx)
        return Children(res, copy=False)
            

    @staticmethod
    def make(*child):
        def proc(children):
            if hasattr(children[0], "__iter__"):
                res = Children()
                for child in children:
                    res.append(proc(child))
                return res
            return Children(children)
        return proc(child)

    @property
    def abspaths(self):
        return Children([child.abspath for child in self])
    
    @property
    def super_dir_names(self):
        return self.map(lambda x: x.super_dir_name)

    
    def __add__(self, x):
        return Children(super().__add__(x), False)
    

    def __len__(self):
        return self.data.__len__()
    

    def __iter__(self):
        return self.data.__iter__()
    
    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return Children(self.data[idx], False)
        return self.data[idx]

    def __setitem__(self, k, v):
        self.data[k] = v
        return self

    def __str__(self) -> str:
        return str(self.data)
    

    def __repr__(self) -> str:
        return self.__str__()

if __name__  == "__main__":

    c = Children([1, 2, 3])
    x = c + Children([2, 3, 4])
    print(x)
    