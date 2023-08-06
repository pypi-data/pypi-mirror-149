import os

from dart_context.dart_context import DartContext
from utilities.url import get_host, get_instance


def open_logs(service, instance, follow, dart_context: DartContext):
    host_instance = instance if instance is not None else get_instance(service, dart_context)
    try:
        container = dart_context.dart_env.service_container_name(service)
    except Exception as e:
        container = service

    options = '-f ' if follow else ' '
    if host_instance is 'local':
        command = f'docker logs {options}{container}'
    else:
        host = get_host(host_instance, dart_context)
        command = f'ssh -t ubuntu@{host} \'docker logs {options}{container}\''

    print(command)
    os.system(command)

def open_debug(service, instance, dart_context: DartContext):
    host_instance = instance if instance is not None else get_instance(service, dart_context)
    try:
        container = dart_context.dart_env.service_container_name(service)
    except Exception as e:
        container = service

    exec_command = f'docker exec -it {container} /bin/bash'

    if host_instance is 'local':
        command = exec_command
    else:
        host = get_host(host_instance, dart_context)
        command = f'ssh -t ubuntu@{host} \'{exec_command}\''
    print(command)
    os.system(command)


def open_psql(dart_context: DartContext):
    host_instance = get_instance('postgres', dart_context)
    try:
        container = dart_context.dart_env.service_container_name('postgres')
    except Exception as e:
        container = 'postgres'

    exec_command = f'docker exec -it {container} psql -d dart_db'

    if host_instance is 'local':
        command = exec_command
    else:
        host = get_host(host_instance, dart_context)
        command = f'ssh -t ubuntu@{host} \'{exec_command}\''
    print(command)
    os.system(command)
