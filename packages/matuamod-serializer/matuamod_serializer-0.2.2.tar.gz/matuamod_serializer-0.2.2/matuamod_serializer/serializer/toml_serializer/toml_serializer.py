from types import NoneType, ModuleType
import toml
from matuamod_serializer.parser.toml_parser.toml_parser import TOML_Parser
from ..base_serializer.base_serializer import BaseSerializer
from matuamod_serializer.dto.dto import DTO, DTO_TYPE
from ..dependencies import dependencies
from matuamod_serializer.parser.toml_parser.toml_parser import TOML_Parser
import inspect


class TOML_Serializer(BaseSerializer):

    _str = ""
    _toml_parser = None


    def __init__(self):
        super().__init__()
        self._toml_parser = TOML_Parser()

    
    def dump(self, obj: any, file_path: str):
        with open(file_path, "w") as file:
            res_str = self.dumps(obj)
            file.write(res_str)


    def dumps(self, obj: any) -> str:
        return self._make_serialize(obj)


    def load(self, file_path: str) -> any:
        with open(file_path, 'r') as file:
            toml_str = file.read()
            return self.loads(toml_str)


    def loads(self, s: str) -> any:
        obj_dict = toml.loads(s)
        return self._toml_parser._make_parse(obj_dict)


    def _add(self, obj: any) -> str:
        self._str = toml.dumps(obj)


    def _make_serialize(self, obj: any) -> str:
        primitive_types = (int, float, bool, str, bytes, NoneType) 
        if type(obj) in primitive_types or obj == None:
            res_dict = self._check_is_first(obj)
        else:
            res_dict = self._inspect(obj)
        self._add(res_dict)
        return (self._str)


    def _check_is_first(self, prim_obj: any) -> dict:
        prim_dict = {}
        if type(prim_obj) in (int, float):
            prim_dict[f'{DTO_TYPE.number}'] = prim_obj
        elif type(prim_obj) == str:
            prim_dict[f'{DTO_TYPE.str}'] = prim_obj
        elif type(prim_obj) == bytes:
            prim_dict[f'{DTO_TYPE.bytes}'] = prim_obj.hex()
        elif type(prim_obj) == bool:   
            prim_dict[f'{DTO_TYPE.bool}'] = prim_obj
        elif type(prim_obj) == NoneType:
            prim_dict[f'{DTO_TYPE.none_type}'] = "null"
        return prim_dict

    
    def _inspect(self, obj: any):
        primitive_types = (int, float, bool, str, bytes, NoneType) 
        if type(obj) in primitive_types or obj == None:
            result = self._inspect_prim_types(obj)
        elif type(obj) in (list, tuple):
            result = self._inspect_list(obj)
        elif type(obj) == dict:
            result = self._inspect_dict(obj)
        elif inspect.isfunction(obj):
            result = self._inspect_func(obj)
        elif inspect.isclass(obj):
            result = self._inspect_class(obj)
        elif type(obj) == ModuleType:
            result = self._inspect_obj_module(obj)
        elif isinstance(obj, object):
            result = self._inspect_obj(obj)
        return result


    def _inspect_prim_types(self, prim_obj: any) -> any:
        if type(prim_obj) == bytes:
            prim_obj = prim_obj.hex()
        return (prim_obj if type(prim_obj) != NoneType else "null")


    def _inspect_list(self, list_obj: list) -> dict:
        list_dict = {}
        list_dict[f'{DTO.dto_type}'] = f'{DTO_TYPE.list}'        
        if list_obj == []:
            return list_dict
        else:
            for i, member in enumerate(list_obj):
                list_dict[f'item_{i}'] = self._inspect(member)
            return list_dict


    def _inspect_dict(self, dict_obj: dict) -> dict:
        res_dict = {}
        res_dict[f'{DTO.dto_type}'] = f'{DTO_TYPE.dict}'
        if dict_obj == {}:
            return res_dict
        else:
            for item in dict_obj.items():
                res_dict[item[0]] = self._inspect(item[1])
            return res_dict
 
    
    def _inspect_func(self, func_obj) -> dict:
        func_dict = {}
        func_dict[f'{DTO.dto_type}'] = f'{DTO_TYPE.func}'
        func_dict[f'{DTO.name}'] = self._inspect(func_obj.__name__)
        globals_dict = dependencies.get_globals(func_obj)
        func_dict[f'{DTO.global_types}'] = self._inspect(globals_dict)
        code_dict = dependencies.get_code_fields(func_obj.__code__)
        func_dict[f'{DTO.code}'] = self._inspect(code_dict)
        func_dict[f'{DTO.closure}'] = self._inspect(func_obj.__closure__)
        return func_dict


    def _inspect_class(self, class_obj: type) -> dict:
        class_dict = {}
        class_dict[f'{DTO.dto_type}'] = f'{DTO_TYPE.class_type}'
        class_dict[f'{DTO.name}'] = self._inspect(class_obj.__name__)
        fields_dict = dependencies.get_class_fields(class_obj)
        class_dict[f'{DTO.fields}'] = self._inspect(fields_dict)
        return class_dict

    
    def _inspect_obj(self, obj):
        obj_dict = {}
        obj_dict[f'{DTO.dto_type}'] = f'{DTO_TYPE.obj_type}'
        obj_dict[f'{DTO.base_class}'] = self._inspect(obj.__class__)
        obj_dict[f'{DTO.fields}'] = self._inspect(obj.__dict__)
        return obj_dict


    def _inspect_obj_module(self, obj_module):
        module_dict = {}
        module_dict[f'{DTO.dto_type}'] = f'{DTO_TYPE.module}'
        module_dict[f'{DTO.name}'] = self._inspect(obj_module.__name__)
        if dependencies.is_std_lib_module(obj_module):
            module_dict[f'{DTO.fields}'] = self._inspect(None)
        else:
            module_fields = dependencies.get_module_fields(obj_module)
            module_dict[f'{DTO.fields}'] = self._inspect(module_fields)
        return module_dict

        