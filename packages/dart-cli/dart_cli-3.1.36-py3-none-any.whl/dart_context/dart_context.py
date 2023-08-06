import json
import os
from typing import Callable

from dart_context.auth_config import AuthConfig
from dart_context.dart_config import DartConfig, DartContextException
from dart_context.dart_environment.dart_environment import DartEnvironment
from dart_context.docker_config import DockerRegistryConfig
from dart_context.kafka_config import KafkaConfig


DEFAULT_TENANTS = list()


class DartContext(DartConfig):
    dart_env: DartEnvironment = DartEnvironment()
    kafka_config: KafkaConfig = KafkaConfig()
    docker_config: DockerRegistryConfig = DockerRegistryConfig()
    auth_config: AuthConfig = AuthConfig()

    aws_profile: str = None
    ssh_key: str = None
    __tenants = None

    def tenants(self) -> list:
        if self.__tenants is None:
            return DEFAULT_TENANTS
        return self.__tenants

    def set_aws_profile(self, p):
        self.aws_profile = p

    def set_ssh_key(self, key_path):
        self.ssh_key = key_path

    def add_tenant(self, tenant: str):
        self.__tenants.append(tenant)

    def add_tenants(self, tenants: list):
        if tenants is not None:
            self.__tenants = self.tenants() + tenants

    def sub_config_fields(self) -> dict[str, 'DartConfig']:
        return {
            'dart_env': self.dart_env,
            'auth_config': self.auth_config,
            'kafka_config': self.kafka_config,
            'docker_config': self.docker_config,
        }

    def primitive_fields(self) -> dict[str, (Callable[[], any], Callable[[any], None])]:
        return {
            'aws_profile': (lambda: self.aws_profile, lambda ap: self.set_aws_profile(ap)),
            'ssh_key': (lambda: self.ssh_key, lambda sk: self.set_ssh_key(sk)),
            'tenants': (lambda: self.__tenants, lambda ts: self.add_tenants(ts)),
        }

    def from_profile(self, profile_name: str) -> None:
        profile_filename = profile_name + '.conf'
        profile_path = os.path.join(os.getenv('HOME'), '.dart', profile_filename)

        try:
            with open(profile_path, 'rt') as profile_file:
                profile_data = json.loads(profile_file.read())
                self.from_dict(profile_data)
        except FileNotFoundError:
            raise DartContextException(f'Unable to open DART configuration profile: {profile_name}')

    def save_profile(self, profile_name: str) -> None:
        profile_filename = profile_name + '.conf'
        dart_path = os.path.join(os.getenv('HOME'), '.dart')
        if not os.path.isdir(dart_path):
            os.mkdir(dart_path)
        profile_path = os.path.join(dart_path, profile_filename)
        profile_data = self.to_dict()

        with open(profile_path, 'wt') as profile_file:
            profile_file.write(json.dumps(profile_data, indent=4))
