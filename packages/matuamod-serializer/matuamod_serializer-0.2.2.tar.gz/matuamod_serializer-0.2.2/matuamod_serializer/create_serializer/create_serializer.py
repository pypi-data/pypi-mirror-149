from ..serializer.base_serializer.base_serializer import BaseSerializer
from ..serializer.json_serializer.json_serializer import JSON_Serializer
from ..serializer.toml_serializer.toml_serializer import TOML_Serializer
from ..serializer.yaml_serializer.yaml_serilizer import YAML_Serializer


SERIALIZERS = {
    "json": JSON_Serializer,
    "toml": TOML_Serializer,
    "yaml": YAML_Serializer
}

def create_serializer(serializer_name: str) -> BaseSerializer:
    if serializer_name in SERIALIZERS:
        return SERIALIZERS[serializer_name]()
    else:
        return None

