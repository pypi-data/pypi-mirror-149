import ssl
from abc import ABC, abstractmethod
from typing import Callable

from dart_context.dart_config import DartConfig, DartConfigException


class KafkaConfigType(DartConfig, ABC):
    """
    Configuration that provides all properties required for creating a kafka
    consumer or producer using the python kafka API
    """

    @abstractmethod
    def kafka_props(self) -> {}:
        pass


class DefaultKafkaConfigType(KafkaConfigType):
    """
    Simple config without any authentication
    """

    def kafka_props(self) -> {}:
        return {
            'api_version': (2, 3, 1),
        }

    def sub_config_fields(self) -> dict[str, DartConfig]:
        return {}

    def primitive_fields(self) -> dict[str, (Callable[[], any], Callable[[any], None])]:
        return {}


class SaslKafkaConfigType(KafkaConfigType):
    kafka_username: str = None
    kafka_password: str = None

    __ssl_context = ssl.create_default_context()

    def set_username(self, un: str) -> None:
        self.kafka_username = un

    def set_password(self, un: str) -> None:
        self.kafka_password = un

    def kafka_props(self) -> {}:
        return {
            'api_version': (2, 3, 1),
            'sasl_plain_username': self.kafka_username,
            'sasl_plain_password': self.kafka_password,
            'security_protocol': 'SASL_SSL',
            'ssl_context': self.__ssl_context,
            'sasl_mechanism': 'PLAIN',
        }

    def sub_config_fields(self) -> dict[str, 'DartConfig']:
        return {}

    def primitive_fields(self) -> dict[str, (Callable[[], any], Callable[[any], None])]:
        return {
            'kafka_username': (lambda: self.kafka_username, lambda un: self.set_username(un)),
            'kafka_password': (lambda: self.kafka_password, lambda pw: self.set_password(pw)),
        }


DEFAULT_CONFIG_TYPE = 'default'


class KafkaConfig(KafkaConfigType):
    """
    Base configuration for kafak integration allowing choice of different kafka configuration
    types (see KafkaConfigType)
    """

    default_config: DefaultKafkaConfigType = DefaultKafkaConfigType()
    sasl_config: SaslKafkaConfigType = SaslKafkaConfigType()

    config_type: str = None

    def set_config_type(self, new_type: str) -> None:
        self.config_type = new_type

    def set_config_type_default(self) -> None:
        self.set_config_type('default')

    def set_config_type_sasl(self) -> None:
        self.set_config_type('sasl')

    # Don't need this, since we'll just override the main
    # kafka_props method
    def __kafka_props(self) -> {}:
        pass

    def kafka_props(self) -> {}:
        if self.config_type is None or self.config_type == 'default':
            return self.default_config.kafka_props()
        elif self.config_type == 'sasl':
            return self.sasl_config.kafka_props()
        else:
            raise DartConfigException(f'invalid kafka configuration type select: {self.config_type}')

    def sub_config_fields(self) -> dict[str, DartConfig]:
        return {
            'default_config': self.default_config,
            'sasl_config': self.sasl_config,
        }

    def primitive_fields(self) -> dict[str, (Callable[[], any], Callable[[any], None])]:
        return {
            'config_type': (lambda: self.config_type, lambda ct: self.set_config_type(ct)),
        }


