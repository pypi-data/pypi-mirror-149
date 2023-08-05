from matuamod_serializer.dto.dto import DTO_TYPE, DTO
from types import CodeType, FunctionType, ModuleType, NoneType
import inspect
import imp

class TOML_Parser():
    
    def _make_parse(self, obj_dict: dict) -> any:
        if len(obj_dict) == 1:
            for item in obj_dict.items():
                obj = self._parse_types(item[1])
        else:
            obj = self._parse_types(obj_dict)
        return obj
    
    
    def _parse_types(self, obj: any) -> any:
        primitive_types = (int, float, bool, str, bytes, NoneType) 
        if type(obj) in primitive_types or obj == None:
            obj = self._parse_prim_type(obj)
        else:
            obj = self._parse_dto(obj)
        return obj


    def _parse_prim_type(self, prim_obj: any) -> any:
        if type(prim_obj) == str:
            if prim_obj == 'null':
                prim_obj = None
        return prim_obj


    def _parse_dto(self, dto_obj: dict) -> any:
        if dto_obj[DTO.dto_type] == DTO_TYPE.list:
            obj = self._parse_list_type(dto_obj)
        elif dto_obj[DTO.dto_type] == DTO_TYPE.dict:
            obj = self._parse_dict_type(dto_obj)
        elif dto_obj[DTO.dto_type] == DTO_TYPE.func:
            obj = self._parse_func_type(dto_obj)
        elif dto_obj[DTO.dto_type] == DTO_TYPE.class_type:
            obj = self._parse_class_type(dto_obj)
        elif dto_obj[DTO.dto_type] == DTO_TYPE.obj_type:
            obj = self._parse_obj_type(dto_obj)
        elif dto_obj[DTO.dto_type] == DTO_TYPE.module:
            obj = self._parse_module(dto_obj)
        return obj


    def _parse_list_type(self, list_obj: dict) -> list:
        list = []
        list_obj.pop(DTO.dto_type)
        for item in list_obj.items():
            list.append(self._parse_types(item[1]))
        return list


    def _parse_dict_type(self, dict_obj: dict) -> dict:
        dict = {}
        dict_obj.pop(DTO.dto_type)
        for item in dict_obj.items():
            dict[self._parse_types(item[0])] = self._parse_types(item[1])
        return dict


    def _parse_func_type(self, func_obj: dict) -> FunctionType:
        func_obj.pop(DTO.dto_type)
        func_name = self._parse_types(func_obj[DTO.name])
        func_closure = self._parse_types(func_obj[DTO.closure])
        func_globals = self._parse_types(func_obj[DTO.global_types])
        code_dict = self._parse_types(func_obj[DTO.code])

        func_code = CodeType(
            code_dict["co_argcount"], code_dict["co_posonlyargcount"],
            code_dict["co_kwonlyargcount"], code_dict["co_nlocals"],
            code_dict["co_stacksize"], code_dict["co_flags"],
            bytes.fromhex(code_dict["co_code"]), tuple(code_dict["co_consts"]),
            tuple(code_dict["co_names"]), tuple(code_dict["co_varnames"]),
            code_dict["co_filename"], code_dict["co_name"],
            code_dict["co_firstlineno"], bytes.fromhex(code_dict["co_lnotab"]),
            tuple(code_dict["co_freevars"]), tuple(code_dict["co_cellvars"]),
        )

        res_func = FunctionType(func_code, func_globals,
                                func_name, func_closure)
        res_func.__globals__["__builtins__"] = __import__("builtins")
        return res_func


    def _parse_class_type(self, class_obj: dict) -> type:
        class_obj.pop(DTO.dto_type)
        class_name = self._parse_types(class_obj[DTO.name])
        class_fields = self._parse_types(class_obj[DTO.fields])
        class_bases = (object,)
        if "__bases__" in class_fields:
            class_bases = tuple(class_fields["__bases__"])
        res_class = type(class_name, class_bases, class_fields)
        return res_class


    def _parse_obj_type(self, obj_type: dict) -> any:
        obj_type.pop(DTO.dto_type)
        base_class = self._parse_types(obj_type[DTO.base_class])
        obj_fields = self._parse_types(obj_type[DTO.fields])

        class_init = base_class.__init__
        if callable(class_init):
            if class_init.__class__.__name__ == 'function':
                delattr(base_class, "__init__")
        obj = base_class()
        obj.__init__ = class_init
        obj.__dict__ = obj_fields
        return obj


    def _parse_module(self, module_obj: dict) -> ModuleType:
        module_name = self._parse_types(module_obj[DTO.name])
        fields_dict = self._parse_types(module_obj[DTO.fields])
        
        module = None
        if fields_dict == None:
            module = __import__(module_name)
        else:
            module = imp.new_module(module_name)
            for field in fields_dict.items():
                setattr(module,field[0],field[1])
        return module
