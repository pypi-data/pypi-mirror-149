from matuamod_serializer.dto.dto import DTO, DTO_TYPE
import yaml
import inspect
from types import NoneType, FunctionType, ModuleType
from ..dependencies import dependencies
from ..base_serializer.base_serializer import BaseSerializer
from matuamod_serializer.parser.yaml_parser.yaml_parser import YAML_Parser 


class YAML_Serializer(BaseSerializer):

    _yaml_parser = None

    def __init__(self):
        super().__init__()
        self._yaml_parser = YAML_Parser()

    
    def dump(self, obj: any, file_path: str):
        with open(file_path, 'w') as file:
            res_str = self.dumps(obj)
            file.write(res_str)

    
    def dumps(self, obj: any):
        return self._make_serialize(obj)


    def load(self, file_path: str):
        with open(file_path, 'r') as file:
            res_str = file.read()
            return self.loads(res_str)


    def loads(self, s: str):
        return self._yaml_parser._make_parse(s)


    def _inspect_types(self, obj: any) -> any:
        prim_types = (int, float, bool, str, bytes, NoneType)
        if type(obj) in prim_types:
            res_obj = self._inspect_prim_type(obj)
        elif type(obj) in (list, tuple):
            res_obj = self._inspect_list(obj)
        elif type(obj) == dict:
            res_obj = self._inspect_dict(obj)
        elif type(obj) == FunctionType:
            res_obj = self._inspect_func(obj)
        elif type(obj) == type:
            res_obj = self._inspect_class(obj)
        elif type(obj) == ModuleType:
            res_obj = self._inspect_module(obj)
        elif isinstance(obj, object):
            res_obj = self._inspect_obj(obj)
        return res_obj


    def _inspect_prim_type(self, prim_obj: any) -> any:
        return prim_obj


    def _inspect_list(self, list_obj: list) -> list: 
        res_list = []
        for item in list_obj:
            res_list.append(self._inspect_types(item))
        return res_list


    def _inspect_dict(self, dict_obj: dict) -> dict:
        res_dict = {}
        res_dict[f'{DTO.dto_type}'] = f'{DTO_TYPE.dict}'
        for item in dict_obj.items():
            res_dict[self._inspect_types(item[0])] = self._inspect_types(item[1])
        return res_dict


    def _inspect_func(self, func_obj: FunctionType) -> dict:
        func_dict = {}
        func_dict[f'{DTO.dto_type}'] = f'{DTO_TYPE.func}'
        func_dict[f'{DTO.name}'] = self._inspect_types(func_obj.__name__)
        globals_dict = dependencies.get_globals(func_obj)
        func_dict[f'{DTO.global_types}'] = self._inspect_types(globals_dict)
        func_code = dependencies.get_code_fields(func_obj.__code__)
        func_dict[f'{DTO.code}'] = self._inspect_types(func_code)
        func_dict[f'{DTO.closure}'] = self._inspect_types(func_obj.__closure__)
        return func_dict


    def _inspect_class(self, class_obj: type) -> dict:
        class_dict = {}
        class_dict[f'{DTO.dto_type}'] = f'{DTO_TYPE.class_type}'
        class_dict[f'{DTO.name}'] = self._inspect_types(class_obj.__name__)
        class_fields = dependencies.get_class_fields(class_obj)
        class_dict[f'{DTO.fields}'] = self._inspect_types(class_fields)
        return class_dict


    def _inspect_obj(self, obj_type: any) -> dict:
        obj_dict = {}
        obj_dict[f'{DTO.dto_type}'] = f'{DTO_TYPE.obj_type}'
        obj_dict[f'{DTO.base_class}'] = self._inspect_types(obj_type.__class__)
        obj_dict[f'{DTO.fields}'] = self._inspect_types(obj_type.__dict__)
        return obj_dict


    def _inspect_module(self, module_obj: ModuleType) -> dict:
        module_dict = {}
        module_dict[f'{DTO.dto_type}'] = f'{DTO_TYPE.module}'
        module_dict[f'{DTO.name}'] = self._inspect_types(module_obj.__name__)
        if dependencies.is_std_lib_module(module_obj): 
            module_dict[f'{DTO.fields}'] = self._inspect_types(None)
        else:
            module_fields = dependencies.get_module_fields(module_obj)
            module_dict[f'{DTO.fields}'] = self._inspect_types(module_fields)
        return module_dict

    
    def _make_serialize(self, obj: any) -> str:
        res_obj = self._inspect_types(obj)
        return yaml.dump(res_obj, sort_keys=False)
        
