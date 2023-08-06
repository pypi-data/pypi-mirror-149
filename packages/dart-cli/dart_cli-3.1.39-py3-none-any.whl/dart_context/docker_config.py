from typing import Callable

from dart_context.dart_config import DartConfig

DEFAULT_DOCKER_REGISTRY_HOST = 'registry.hub.docker.com'
DEFAULT_DOCKER_REGISTRY_NAMESPACE = '/twosixlabsdart'


class DockerRegistryConfig(DartConfig):
    """
    Configuration for connecting with docker registry to pull deployment utilties.
    Used for TST deployment only.
    """

    docker_username: str = None
    docker_password: str = None
    docker_registry_host: str = None
    docker_namespace: str = None

    def set_docker_username(self, username: str) -> None:
        self.docker_username = username

    def set_docker_password(self, password: str) -> None:
        self.docker_password = password

    def set_docker_registry_host(self, registry_host: str) -> None:
        self.docker_registry_host = registry_host

    def set_docker_namespace(self, namespace: str) -> None:
        self.docker_namespace = namespace

    def sub_config_fields(self) -> dict[str, DartConfig]:
        return {}

    def primitive_fields(self) -> dict[str, (Callable[[], any], Callable[[any], None])]:
        return {
            'docker_username': (lambda: self.docker_username, lambda x: self.set_docker_username(x)),
            'docker_password': (lambda: self.docker_password, lambda x: self.set_docker_password(x)),
            'docker_registry_host': (lambda: self.docker_registry_host, lambda x: self.set_docker_registry_host(x)),
            'docker_namespace': (lambda: self.docker_namespace, lambda x: self.set_docker_namespace(x)),
        }




