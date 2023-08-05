from modulefinder import Module
from matuamod_serializer.parser.json_parser.json_parser import JSON_Parser
from ..base_serializer.base_serializer import BaseSerializer
from matuamod_serializer.dto.dto import DTO, DTO_TYPE
from ..dependencies import dependencies
import inspect
from types import ModuleType, NoneType


class JSON_Serializer(BaseSerializer):

    _str = ""
    _json_parser = None
 

    def __init__(self):
        super().__init__()
        self._json_parser = JSON_Parser()


    def dump(self, obj: any, file_path: str):
        file = open(file_path, "w")
        _str = self.dumps(obj)
        file.write(_str)
        file.close()


    def dumps(self, obj: any) -> str:
        self._str = ""
        self._inspect(obj)
        return self._str


    def load(self, file_path: str) -> any:
        obj = None
        file = open(file_path, "r")
        _str = file.read()
        obj = self.loads(_str)
        return obj


    def loads(self, s: str) -> any:
        return self._json_parser._parse(s)


    def _add(self, type_str: str):
        self._str += type_str


    def _inspect(self, obj):
        primitive_types = (int, float, bool, str, bytes)
        if type(obj) in primitive_types:
            self._inspect_primitive_type(obj)
        elif type(obj) in (tuple, list):
            self._inspect_list_tuple_type(obj)
        elif obj == None:
            self._add("null")
        else:
            self._add("{")
            if type(obj) == dict:
                self._inspect_dict_type(obj)
            elif inspect.isfunction(obj):
                self._inspect_func_type(obj)
            elif inspect.isclass(obj):
                self._inspect_class_type(obj)
            elif type(obj) == ModuleType:
                self._inspect_obj_module(obj)
            elif isinstance(obj, object):
                self._inspect_obj_type(obj)
            self._add("}")


    def _inspect_primitive_type(self, prim_obj):
        prim_obj_type = type(prim_obj)
        if prim_obj_type in (int, float):
            self._add(f'{prim_obj}')
        elif prim_obj_type == bool:
            if prim_obj:
                bool_value = "true"
            else:
                bool_value = "false"
            self._add(f'{bool_value}')
        elif prim_obj_type == str:
            self._add(f'"{prim_obj}"')
        elif prim_obj_type == bytes:
            hexademical = prim_obj.hex()
            self._add(f'"{hexademical}"')


    def _inspect_list_tuple_type(self, obj):
        if(len(obj)) == 0:
            self._add('[]')
        else:
            self._add('[')
            for i, part_obj in enumerate(obj):
                if i != 0:
                    self._add(',')
                self._inspect(part_obj)
            self._add(']')


    def _inspect_dict_type(self, dict_obj: dict):
        self._add(f'"{DTO.dto_type}": "{DTO_TYPE.dict}"')
        if len(dict_obj) >= 1:
            self._add(",")
            is_first_el = True
            i = 0

        for key, value in dict_obj.items():
            if is_first_el != True:
                self._add(',')
            self._inspect(key)
            self._add(': ')
            self._inspect(value)
            is_first_el = False


    def _get_code(self, func_obj):
        code_obj = func_obj.__code__
        self._add(f'"{DTO.code}": ')
        self._add('{')
        self._add(f'"{DTO.dto_type}": "{DTO_TYPE.code}",')
        self._add(f'"{DTO.fields}": ')
        curr_code_dict = dependencies.get_code_fields(code_obj)
        self._inspect(curr_code_dict)
        self._add('}')


    def _inspect_func_type(self, func_obj):
        self._add(f'"{DTO.dto_type}": "{DTO_TYPE.func}",')
        self._add(f'"{DTO.name}": "{func_obj.__name__}",')
        self._add(f'"{DTO.global_types}": ')
        curr_globals_dict = dependencies.get_globals(func_obj)
        self._inspect(curr_globals_dict)
        self._add(',')
        self._get_code(func_obj)
        self._add(',')
        self._add(f'"{DTO.closure}": "{func_obj.__closure__}"')


    def _inspect_class_type(self, class_obj):
        fields_dict = dependencies.get_class_fields(class_obj)
        self._add(f'"{DTO.dto_type}": "{DTO_TYPE.class_type}",')
        self._add(f'"{DTO.name}": "{class_obj.__name__}",')
        self._add(f'"{DTO.fields}": ')
        self._inspect(fields_dict)


    def _inspect_obj_type(self, obj):
        self._add(f'"{DTO.dto_type}": "{DTO_TYPE.obj_type}",')
        self._add(f'"{DTO.base_class}": ')
        self._inspect(obj.__class__)
        self._add(",")
        self._add(f'"{DTO.fields}": ')
        self._inspect(obj.__dict__)


    def _inspect_obj_module(self, obj_module):
        self._add(f'"{DTO.dto_type}": "{DTO_TYPE.module}",')
        self._add(f'"{DTO.name}": "{obj_module.__name__}",')
        self._add(f'"{DTO.fields}": ')
        if dependencies.is_std_lib_module(obj_module):
            self._inspect(None)
        else:
            module_fields = dependencies.get_module_fields(obj_module)
            self._inspect(module_fields)
