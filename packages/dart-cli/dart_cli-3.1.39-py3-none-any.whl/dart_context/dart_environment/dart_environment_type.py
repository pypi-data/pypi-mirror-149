from abc import abstractmethod, ABC

from dart_context.dart_config import DartConfig


class DartEnvironmentType(DartConfig, ABC):
    """
    Defines a configuration for a given deployment environment (default, custom, tst)
    Basically, provides methods to resolve hosts (hostname/IP), urls, and container names for all services.
    """

    @abstractmethod
    def instance_host(self, instance: str) -> str:
        """
        Get the hostname or IP for an instance type
        :param instance: name/id of instance
        :return: hostname or IP address
        """

    @abstractmethod
    def service_instance(self, service: str) -> str:
        """
        Get the instance on which a service is hosted
        :param service:
        :return: instance name/id
        """

    @abstractmethod
    def service_base_url(self, service: str, direct: bool = False) -> str:
        """
        Get the base url for a service -- this can optionally be distinguished in to two different URLs, one for a
        direct connection, and one for a proxied connection
        :argument service: Name of the service (e.g., corpex, forklift, elasticsearch)
        :argument direct: True if this is for a direct (unproxied) connection to the service (e.g. for testing)
        :return: url scheme (e.g. http or https)
        """

    @abstractmethod
    def service_container_name(self, service: str) -> str:
        """
        Get the container name for a service (used for logging and any utilities that require
        exec'ing into a container (e.g., psql).
        :param service: Name of the service (e.g., corpex, forklift, elasticsearch)
        :return: name of the service's container
        """