from dataclasses import dataclass


@dataclass
class DTO():
    dto_type = "dto_type"
    name = "name"
    code = "code"
    fields = "fields"
    global_types = "globals"
    closure = "closure"
    base_class = "base_class"

@dataclass
class DTO_TYPE():
    obj_type = "obj"
    func = "func"
    code = "code"
    module = "module"
    list = "list"
    dict = "dict"
    class_type = "type"
    number = "number"
    str = "str"
    bytes = "bytes"
    bool = "bool"
    none_type = "none"
    