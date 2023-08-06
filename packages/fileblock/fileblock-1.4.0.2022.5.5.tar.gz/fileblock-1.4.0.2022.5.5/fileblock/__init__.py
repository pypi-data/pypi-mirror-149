from .Block import Block
from .Children import Children
from .btype import FILE, DIR
from .utils import *
def make_children(*child) -> Children:
    return Children.make(child)

def unfold(*iter):
    def f(iter):
        res = Children()
        for cell in iter:
            if hasattr(cell, "__iter__"):
                res += f(cell)
            else:
                res.append(cell)
        return res
    return f(iter)

