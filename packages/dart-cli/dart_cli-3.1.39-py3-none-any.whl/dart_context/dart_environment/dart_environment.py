from abc import ABC, abstractmethod
from typing import Callable

from dart_context.dart_config import DartConfig, DartConfigException
from dart_context.dart_environment.dart_environment_type import DartEnvironmentType
from dart_context.dart_environment.env_type_custom import CustomDartEnvironmentType
from dart_context.dart_environment.env_type_default import DefaultDartEnvironmentType
from dart_context.dart_environment.env_type_tst import TstAwsDartEnvironmentType


DEFAULT_DART_ENV_TYPE = 'default'


class DartEnvironment(DartEnvironmentType):
    """
    Central configuration for DART's deployment environment. Provides three different general means of
    configuring this (each being an instance of DartEnvironmentType): default (hard-coded config for
    "Dart-In-A-Box," tst (Two Six Tech specific deployment setup), and custom (allows defining a
    configuration by defining dicts mapping services and instances to required data)
    """

    default_env = DefaultDartEnvironmentType()
    tst_env = TstAwsDartEnvironmentType()
    custom_env = CustomDartEnvironmentType()

    __env_type: str = None

    def env_type(self) -> str:
        if self.__env_type is None:
            return DEFAULT_DART_ENV_TYPE
        return self.__env_type

    def is_default(self) -> bool:
        return self.env_type() == DEFAULT_DART_ENV_TYPE

    def is_tst(self) -> bool:
        return self.env_type() == 'tst'

    def is_custom(self) -> bool:
        return self.env_type() == 'custom'

    def set_env_type(self, et: str) -> None:
        self.__env_type = et

    def sub_config_fields(self) -> dict[str, DartConfig]:
        return {
            'tst_env': self.tst_env,
            'custom_env': self.custom_env,
            'default_env': self.default_env,
        }

    def primitive_fields(self) -> dict[str, (Callable[[], any], Callable[[any], None])]:
        return {
            'env_type': (lambda: self.__env_type, lambda et: self.set_env_type(et)),
        }

    def __get_environment_type(self) -> DartEnvironmentType:
        if self.env_type() == 'custom':
            return self.custom_env
        elif self.env_type() == 'tst':
            return self.tst_env
        elif self.env_type() == 'default':
            return self.default_env
        else:
            raise DartConfigException(f'unknown deployment environment type: {self.env_type()}. Supported values are "custom", "tst", and "default"')

    def instance_host(self, instance: str) -> str:
        return self.__get_environment_type().instance_host(instance)

    def service_instance(self, service: str) -> str:
        return self.__get_environment_type().service_instance(service)

    def service_base_url(self, service: str, direct: bool = False) -> str:
        return self.__get_environment_type().service_base_url(service, direct)

    def service_container_name(self, service: str) -> str:
        return self.__get_environment_type().service_container_name(service)
