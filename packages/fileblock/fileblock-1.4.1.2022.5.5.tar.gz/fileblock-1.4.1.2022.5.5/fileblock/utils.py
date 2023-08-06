from .Children import Children
from .Block import Block
from .btype import DIR, FILE, __BaseType__

def get_path(children:Children, force_abs=False):
    """返回Children内所有block的路径"""
    if force_abs:
        res = children.map(lambda x: x.abspath)
    else:
        res = children.map(lambda x: x.path)
    return res

def type_filter(children:Children, __type:__BaseType__)->Children:
    def dfs(x):
        return Children([
            dfs(cell) if hasattr(cell, "__iter__") else cell
            for cell in x
            if hasattr(cell, "__iter__") or (type(cell)==Block and cell.btype==__type)
        ])
    return dfs(children)

def file_filter(children:Children)->Children:
    """返回Children中的所有FILE类型Block"""
    res = type_filter(children, FILE)
    return res

def dir_filter(children:Children)->Children:
    """返回Children中的所有DIR类型Block"""
    res = type_filter(children, DIR)
    return res

def remove(target:Children):
    if type(target) == Children:
        target.map(lambda x: x.remove())
    elif type(target) == Block:
        target.remove()
    else:
        raise ValueError(target," cannot be removed!")