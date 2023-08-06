from typing import Callable

from dart_context.dart_config import DartConfig, DartConfigException
from dart_context.dart_environment.dart_environment_type import DartEnvironmentType


class CustomDartEnvironmentType(DartEnvironmentType):
    """
    Define a custom dart deployment environment configuration by providing JSON mappings of
    services and instances to hostnames/IPs and other connection data
    """

    # Format: {'instance-name':'hostname/IP'}
    instance_mapping: dict[str, str] = None

    # Format:
    # {
    #   'service-name': {
    #       'instance': 'instance-name',
    #       'port': 8080,
    #       'base_path': '/dart/api/v1/service-name', # this format is default, if base_path is missing
    #       'proxied_url': 'override-url-from-instance-host-and-port',
    #       'container_name': 'service-name'
    #   }
    # }
    service_mapping: {} = None

    def set_instance_mapping(self, im: dict[str, str]) -> None:
        self.instance_mapping = im

    def set_service_mapping(self, sm: {}) -> None:
        self.service_mapping = sm

    def instance_host(self, instance: str) -> str:
        if self.instance_mapping is not None and instance in self.instance_mapping:
            return self.instance_mapping[instance]
        raise DartConfigException(
            f'instance mapping for custom dart environment configuration does not contain required instance {instance}')

    def service_instance(self, service: str) -> str:
        if self.service_mapping is not None and service in self.service_mapping:
            if 'instance' in self.service_mapping[service]:
                return self.service_mapping[service]['instance']
            raise DartConfigException(f'service mapping for custom dart environment configuration does not provide instance for service {service}')
        raise DartConfigException(
            f'service mapping for custom dart environment configuration does not contain required service {service}'
        )

    def service_port(self, service: str) -> int:
        if self.service_mapping is not None and service in self.service_mapping:
            if 'port' in self.service_mapping[service]:
                return self.service_mapping[service]['port']
            raise DartConfigException(f'service mapping for custom dart environment configuration does not provide port for service {service}')
        else:
            raise DartConfigException(f'service mapping for custom dart environment configuration does not contain required service {service}')

    def service_base_path(self, service: str) -> str:
        if self.service_mapping is not None and service in self.service_mapping:
            if 'base_path' in self.service_mapping[service]:
                return self.service_mapping[service]['base_path']
            return f'/dart/api/v1/{service}'
        else:
            raise DartConfigException(f'service mapping for custom dart environment configuration does not contain required service {service}')

    def service_container_name(self, service: str) -> str:
        if self.service_mapping is not None and service in self.service_mapping:
            if 'container_name' in self.service_mapping[service]:
                return self.service_mapping[service]['container_name']
            raise DartConfigException(f'service mapping for custom dart environment configuration does not provide container name for service {service}')
        else:
            raise DartConfigException(f'service mapping for custom dart environment configuration does not contain required service {service}')

    def construct_base_url(self, service: str) -> str:
        instance = self.service_instance(service)
        host = self.instance_host(instance)
        port = self.service_port(service)
        base_path = self.service_base_path(service)
        return f'http://{host}:{port}{base_path}'

    def service_base_url(self, service: str, direct: bool = False) -> str:
        if self.service_mapping is not None and service in self.service_mapping:
            if not direct and 'proxied_url' in self.service_mapping[service]:
                return self.service_mapping[service]['proxied_url']

            return self.construct_base_url(service)
        else:
            raise DartConfigException(f'service mapping for custom dart environment configuration does not contain required service {service}')

    def sub_config_fields(self) -> dict[str, DartConfig]:
        return {}

    def primitive_fields(self) -> dict[str, (Callable[[], any], Callable[[any], None])]:
        return {
            'instance_mapping': (lambda: self.instance_mapping, lambda x: self.set_instance_mapping(x)),
            'service_mapping': (lambda: self.service_mapping, lambda x: self.set_service_mapping(x)),
        }
