from typing import Callable

from dart_context.dart_config import DartConfigException
from dart_context.dart_environment.dart_environment_type import DartEnvironmentType


class TstAwsDartEnvironmentType(DartEnvironmentType):
    image_prefix: str = None
    ssh_user: str = None
    env: str = None
    aws_environment: str = None  # dart, prod
    deploy_profile: str = None  # Which profile is used by cdk (generally will be dart-distributed)
    project_id: str = None
    pipeline_version: str = None  # tag of the docker image used for provision/deploy

    def set_image_prefix(self, ip):
        self.image_prefix = ip

    def set_ssh_user(self, new_user) -> None:
        self.ssh_user = new_user

    def set_env(self, e):
        self.env = e

    def set_aws_environment(self, e):
        self.aws_environment = e

    def set_deploy_profile(self, p):
        self.deploy_profile = p

    def set_project_id(self, id):
        self.project_id = id

    def set_pipeline_version(self, version):
        self.pipeline_version = version

    def sub_config_fields(self) -> dict[str, 'DartConfig']:
        return {}

    def primitive_fields(self) -> dict[str, (Callable[[], any], Callable[[any], None])]:
        return {
            'image_prefix': (lambda: self.image_prefix, lambda x: self.set_image_prefix(x)),
            'ssh-user': (lambda: self.ssh_user, lambda su: self.set_ssh_user(su)),
            'env': (lambda: self.env, lambda x: self.set_env(x)),
            'aws_environment': (lambda: self.aws_environment, lambda x: self.set_aws_environment(x)),
            'deploy_profile': (lambda: self.deploy_profile, lambda x: self.set_deploy_profile(x)),
            'project_id': (lambda: self.project_id, lambda x: self.set_project_id(x)),
            'pipeline_version': (lambda: self.pipeline_version, lambda x: self.set_pipeline_version(x)),
        }

    __instances = {
        'rest': {
            'suffix': '-ingest-pipeline-rest-1',
        },
        'streaming': {
            'suffix': '-ingest-pipeline-streaming-1',
        },
        'analytics': {
            'suffix': '-ingest-pipeline-analytics-1',
        },
        'data-master': {
            'suffix': '-ingest-pipeline-data-master-1',
        },
        'data-worker': {
            'suffix': '-ingest-pipeline-data-worker-1',
        },
        'batch-master': {
            'suffix': '-batch-master',
        },
        'batch-worker': {
            'suffix': '-batch-worker-1',
        },
        'batch-worker-1': {
            'suffix': '-batch-worker-1',
        },
        'batch-worker-2': {
            'suffix': '-batch-worker-2',
        },
        'main': {
            'suffix': '',
        }
    }

    __domains = {
        'prod': 'prod.dart.worldmodelers.com',
        'dart': 'dart.worldmodelers.com',
    }

    __services = {
        'cdr-retrieval': {
            'instance': 'rest',
            'port': 8090,
            'proxied': True,
            'type': 'dart',
            'path_name': 'cdrs',
            'container': 'cdr-retrieval',
        },
        'corpex': {
            'instance': 'rest',
            'port': 8088,
            'proxied': True,
            'type': 'dart',
            'container': 'corpex',
        },
        'forklift': {
            'instance': 'rest',
            'port': 8091,
            'proxied': True,
            'type': 'dart',
            'container': 'forklift',
        },
        'reprocess': {
            'instance': 'rest',
            'port': 6309,
            'type': 'dart',
            'container': 'daydream-nation',
        },
        'ladle': {
            'instance': 'streaming',
            'port': 8080,
            'container': 'ladle',
        },
        'readers-output': {
            'instance': 'rest',
            'port': 13337,
            'proxied': True,
            'type': 'dart',
            'container': 'readers-output',
            'path_name': 'readers',
        },
        'postgres': {
            'instance': 'data-master',
            'port': 5432,
            'type': 'database',
            'container': 'dart-postgres',
        },
        'keycloak': {
            'instance': 'rest',
            'port': 8090,
            'proxied': 'rest',
            'container': 'keycloak-dart',
        },
        'tenants': {
            'instance': 'rest',
            'port': 8080,
            'proxied': True,
            'type': 'dart',
            'container': 'dart-tenants',
        },
        'ontologies': {
            'instance': 'rest',
            'port': 8084,
            'proxied': True,
            'container': 'ontology-registry',
            'path': 'ontologies',
            'type': 'dart',
        },
        'users': {
            'instance': 'rest',
            'port': 8081,
            'proxied': True,
            'type': 'dart',
            'container': 'dart-users',
        },
        'dart': {
            'instance': 'streaming',
            'type': 'restless',
            'container': 'dart-3',
        },
        'elasticsearch': {
            'instance': 'data-master',
            'port': 9200,
            'type': 'database',
            'container': 'dart-es-master',
        },
    }

    def get_domain(self) -> str:
        if self.aws_environment in self.__domains:
            return self.__domains[self.aws_environment]
        raise DartConfigException(f'{self.aws_environment} is not a valid aws environment (should be prod or dart)')

    def instance_host(self, instance: str) -> str:
        if instance in self.__instances:
            if self.env is not None:
                return self.env + self.__instances[instance]['suffix'] + '.' + self.get_domain()
            raise DartConfigException('Dart deployment environment name is not configured. Use -e or --env option.')
        raise DartConfigException(f'{instance} is not a recognized instance')

    def service_instance(self, service: str) -> str:
        if service in self.__services:
            return self.__services[service]['instance']
        raise DartConfigException(f'{service} is not recognized service')

    def service_base_url(self, service: str, direct: bool = False) -> str:
        if service in self.__services:
            service_data = self.__services[service]
            instance = service_data['instance']
            full_host = self.instance_host(instance)
            if 'proxied' in service_data and service_data['proxied']:
                host = self.env + '.' + self.get_domain()
                scheme = 'https'
                port_suffix = ''
            else:
                host = full_host
                scheme = 'http'
                port_suffix = f':{service_data["port"]}'
            if 'type' in service_data and service_data['type'] == 'dart':
                path = '/dart/api/v1/' + (service_data['path_name'] if 'path_name' in service_data else service)
            else:
                path = ''
            url = f'{scheme}://{host}{port_suffix}{path}'
            return url

        raise DartConfigException(f'{service} is not recognized service')

    def service_container_name(self, service: str) -> str:
        if service in self.__services:
            return self.__services[service]['container']
        return service
