# File Block

[Programe](https://github.com/miaobuao/fileblock)

简化文件处理 - *simplify file processing*

<!-- [](https://github.com/miaobuao/fileblock/todo.md) -->
## Installing from pip

pip 安装

```shell
pip install fileblock
```

清华源安装

```shell
pip install fileblock -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## How to use

```python
import fileblock as fb
from fileblock import Block, Children
```

### Block

#### Create Block

```python
file_block = Block("./") # 创建一个Block
```

| 参数 | 类型   | 返回值 | 描述                  |
| ---- | ------ | ------ | --------------------- |
| name | string | None   | 创建 block 的逻辑位置 |

```text
Tips:
  @path 不一定是真实存在的文件或者文件夹路径
```

#### block.sub_block(path)

| 参数 | 类型   | 返回值 | 描述                    |
| ---- | ------ | ------ | -----------------------|
| path | string | Block  | 相对于 block 的相对路径 |

#### block.append(name, type=FILE)

| 参数 | 类型   | 描述                    |
| ---- | ------ | -----------------------|
| name | string   | 相对于 block 的相对路径 |
| type | btype.FILE / btype.DIR | 需要添加的节点类型 |

返回新生成节点的Block对象

```text
Tips:
    当type == FILE时，若name形如x1/x2, 则会新建x1文件夹，返回的是x2的Block对象，而不是x1
```

#### block.join_path(path)

| 参数 | 类型   |描述                    |
| ---- | ------ |-----------------------|
| path | string| 需要拼接的文件/文件夹路径 |

返回拼接后的路径

#### block.remove()

说明：

如果该 block 对象是真实存在的文件/文件夹, 则从磁盘上永久删除该文件/文件夹

#### block.moveTo(target)

| 参数 | 类型   |描述                    |
| ---- | ------ |-----------------------|
| target | Block| 一个类型为Dir的Block对象|

如果block存在，则会把其中的文件与文件夹移动到target对应的文件夹内

#### block.copyTo(target: Block)

| 参数 | 类型   |描述                    |
| ---- | ------ |-----------------------|
| target | Block| 一个类型为Dir的Block对象|

把 Block 及其 Children 都拷贝如 target 中

#### block.cut(\*rates:int|float)->list[Children]

| 参数 | 类型   |描述                    |
| ---- | ------ |-----------------------|
| rates | int/float| 需要划分的比重|

**🌰举个例子:**

文件夹里如果有n个文件，想要划分成7:3，那参数就是7, 3，也就是block.cut(7, 3)

如果想要分成1:2:3，那就block.cut(1, 2, 3)

返回值时一个列表，其中的元素是划分好的Children类型

#### block.get_file_contents() -> bytes

如果block时文件，则返回该文件的bytes内容

#### block.leaves

Block文件树的叶子节点构成的[Children](#children)集合

#### block.isfile -> bool

当block存在，且为文件时等于True

#### block.isdir -> bool

当block存在，且为文件夹时为True

#### block.exists -> bool

当block存在时为True

#### block.children -> Children[Block]

返回block对象包含的子文件与子文件夹构成的[Children](#children)集合

#### block.btype ->  __FILE | __DIR | None

返回该Block对象的类型 ```FILE``` | ```DIR``` | ```None```
### Children

*Children类继承自list*
#### children.abspaths -> list[str]

返回所有Block的绝对路径

#### children.shuffle -> Children:

返回打乱顺序的Children，不改变本身内容

#### 加法

```python
c1 = Children()
c2 = Children()
c3 = c1 + c2 # type(c3) == Children
```

## License

[Apache 2.0](https://github.com/miaobuao/fileblock/blob/main/LICENSE)

