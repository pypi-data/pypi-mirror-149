import json
from abc import ABC, abstractmethod
from typing import Callable


class DartContextException(Exception):
    """For exceptions related to dart context"""

    def __init__(self, *args):
        super().__init__(args)


class DartConfigException(DartContextException):
    """For exceptions related to dart configuration"""

    def __init__(self, problem):
        self.problem = problem
        self.message = f'Invalid configuration due to {problem}'
        super().__init__(self.message)


class MissingParameterException(DartConfigException):
    def __init__(self, param):
        self.param = param
        self.message = f'missing parameter: {self.param}. This can be set either on the command line or in a configuration profile'
        super().__init__(self.message)


class DartConfig(ABC):
    """Base class for configuration: requires ability to read/write config to dict"""

    @abstractmethod
    def sub_config_fields(self) -> dict[str, 'DartConfig']:
        """Build a dictionary mapping field names to a nested dart config class"""

    @abstractmethod
    def primitive_fields(self) -> dict[str, (Callable[[], any], Callable[[any], None])]:
        """Build a dictionary mapping a field name to a getter and a setter"""

    def from_dict(self, config_dict: dict[str, any]) -> None:
        """Populate fields from a dictionary"""
        sub_configs = self.sub_config_fields()
        primitives = self.primitive_fields()
        for field in config_dict:
            if field in sub_configs:
                sub_configs[field].from_dict(config_dict[field])
            elif field in primitives:
                primitives[field][1](config_dict[field])

    def to_dict(self) -> dict[str, any]:
        """Generates dict of all configuration fields"""
        sub_configs = self.sub_config_fields()
        primitives = self.primitive_fields()
        result = {}
        for field in primitives:
            field_value = primitives[field][0]()
            if field_value is not None:
                result[field] = field_value
        for field in sub_configs:
            field_value = sub_configs[field].to_dict()
            if len(field_value) > 0:
                result[field] = field_value
        return result

    def to_json(self) -> str:
        """Write configuration to string"""
        return json.dumps(self.to_dict(), indent=4)

    def from_json(self, config_json: str) -> None:
        """Populate fields from a json string"""
        self.from_dict(json.loads(config_json))