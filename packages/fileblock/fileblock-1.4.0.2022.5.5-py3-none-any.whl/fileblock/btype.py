class __BaseType__:
    
    def __init__(self, name) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, __o) -> bool:
        if type(__o) == str:
            return __o == self.name
        elif type(__o) == __BaseType__:
            return __o.name == self.name
        return False

# class __DirType__(__BaseType__):
    
#     def __init__(self) -> None:
#         super().__init__("Dir")

# class __FileType__(__BaseType__):
    
#     def __init__(self) -> None:
#         super().__init__("File")


# FILE = __FileType__()
# DIR = __DirType__()

FILE = __BaseType__("File")
DIR = __BaseType__("Dir")

if __name__ == "__main__":
    print(FILE.__dict__)