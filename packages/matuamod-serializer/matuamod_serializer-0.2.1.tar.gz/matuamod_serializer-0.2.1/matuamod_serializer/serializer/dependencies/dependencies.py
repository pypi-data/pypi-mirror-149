import inspect
from matuamod_serializer.dto.dto import DTO, DTO_TYPE
from types import NoneType, WrapperDescriptorType, MethodDescriptorType, BuiltinFunctionType, MappingProxyType, GetSetDescriptorType, ModuleType
import sys
import imp

def get_globals(func_obj) -> dict:
    globals_type = func_obj.__globals__
    curr_globals_dict = dict()
    code_obj = func_obj.__code__

    for key, value in globals_type.items():
        if key in code_obj.co_names:
            curr_globals_dict.update({key: value})
    return curr_globals_dict


def get_code_fields(code_obj) -> dict:
    curr_code_dict = dict()
    variables = (
        "co_nlocals", "co_argcount",
        "co_varnames", "co_names",
        "co_cellvars", "co_freevars",
        "co_posonlyargcount", "co_kwonlyargcount",
        "co_firstlineno", "co_lnotab",
        "co_stacksize", "co_code", "co_name",
        "co_consts", "co_flags", "co_filename"
    )

    for member in inspect.getmembers(code_obj):
        if member[0] in variables:
            curr_code_dict.update({member[0]: member[1]})
    return curr_code_dict


def get_class_fields(class_obj) -> dict:
    fields_dict = dict()
    if class_obj == type:
        fields_dict["__bases__"] = []
    else:
        members = inspect.getmembers(class_obj)

        for member in members:
            if type(member[1]) not in (
                WrapperDescriptorType,
                MethodDescriptorType,
                BuiltinFunctionType,
                MappingProxyType,
                GetSetDescriptorType
            ) and member[0] not in (
                "__mro__", "__base__", "__basicsize__",
                "__class__", "__dictoffset__", "__name__",
                "__qualname__", "__text_signature__", "__itemsize__",
                "__flags__", "__weakrefoffset__"
            ):
                fields_dict[member[0]] = member[1]
    return fields_dict


def get_module_fields(obj_module: ModuleType) -> dict:
    module_fields = {}
    for member in inspect.getmembers(obj_module):
        if not member[0].startswith("__"):
            module_fields[member[0]] = member[1]
    return module_fields


def is_std_lib_module(obj_module: ModuleType):
    libs_path = sys.path[2]
    module_path = imp.find_module(obj_module.__name__)[1]
    if obj_module.__name__ in sys.builtin_module_names:
        return True
    elif libs_path in module_path:
        return True
    elif "site-packages" in module_path:
        return True
    else:
        return False