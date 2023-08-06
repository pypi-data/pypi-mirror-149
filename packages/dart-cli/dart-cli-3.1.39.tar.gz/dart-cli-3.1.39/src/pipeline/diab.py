import os
import uuid

from dart_context.dart_context import DartContext


def compose_file_url(context: DartContext) -> str:
    version = context.dart_env.default_env.version
    if version is None:
        branch_segment = 'master'
    elif len(version.split('.')) == 3:
        branch_segment = f'v{version.strip().lstrip("v")}'
    else:
        branch_segment = version.strip()

    return f'https://raw.githubusercontent.com/twosixlabs-dart/dart-in-the-box/{branch_segment}/dart-standalone.yml'


def clean_command(data_root: str):
    data_dir = f'{data_root}/data'
    return f'sudo rm -rf {data_dir}'


def initialize_data_command(data_root: str, user):
    data_dir = f'{data_root}/data'
    es_dirs = f'{data_dir}/dart-es-master {data_dir}/dart-es-replica-1 {data_dir}/dart-es-replica-2'
    return f'mkdir -p {es_dirs}; chown -R {user}: {data_dir}'


def check_data_command(context: DartContext):
    data_dir = './data'
    return f'[ -d  "{data_dir}/dart-es-master" ] && [ -d "{data_dir}/dart-es-replica-1" ] && [ -d "{data_dir}/dart-es-replica-2" ]'


def dc_up_command(context: DartContext):
    proxy_host_str = f'PROXY_HOSTNAME={context.dart_env.default_env.host} ' if context.dart_env.default_env.host is not None else ''
    return proxy_host_str + 'docker-compose up -d'

def dc_pull_command():
    return 'docker-compose pull'


def command_with_docker_compose(context: DartContext, cmd: str) -> str:
    data_root = context.dart_env.default_env.data_dir if context.dart_env.default_env.data_dir is not None else '.'
    return f'cd {data_root}; rm -f docker-compose.yml; curl {compose_file_url(context)} --output docker-compose.yml; {cmd}; rm -f docker-compose.yml'


def deploy_diab(context: DartContext) -> None:
    data_root = context.dart_env.default_env.data_dir if context.dart_env.default_env.data_dir is not None else '.'
    user = context.dart_env.default_env.user if context.dart_env.default_env.user is not None else '$USER'
    clean_cmd = clean_command(data_root)
    init_cmd = initialize_data_command(data_root, user)
    deploy_cmd = command_with_docker_compose(context, f'docker-compose down; {clean_cmd}; {init_cmd}; {dc_up_command(context)}')
    execute(context, deploy_cmd)


def start_diab(context: DartContext) -> None:
    check_cmd = check_data_command(context)
    start_cmd = f'{dc_pull_command()} && {dc_up_command(context)}'
    conditional_cmd = f'{check_cmd} && {start_cmd} || echo "Unable to start services: data directory is uninitialized"'
    full_cmd = command_with_docker_compose(context, conditional_cmd)
    execute(context, full_cmd)


def stop_diab(context: DartContext) -> None:
    stop_cmd = 'docker-compose down'
    full_cmd = command_with_docker_compose(context, stop_cmd)
    execute(context, full_cmd)


def clean_diab(context: DartContext) -> None:
    data_root = context.dart_env.default_env.data_dir if context.dart_env.default_env.data_dir is not None else '.'
    cmd = clean_command(data_root)
    execute(context, cmd)


def destroy_diab(context: DartContext) -> None:
    data_root = context.dart_env.default_env.data_dir if context.dart_env.default_env.data_dir is not None else '.'
    clean_cmd = clean_command(data_root)
    dc_down_cmd = 'docker-compose down'
    destroy_cmd = command_with_docker_compose(context, f'{dc_down_cmd}; {clean_cmd}')
    execute(context, destroy_cmd)


def execute(dart_context: DartContext, cmd: str) -> None:
    if dart_context.dart_env.default_env.host is None:
        command = cmd
    else:
        host = dart_context.dart_env.default_env.host
        id_opt = f'-i ~/.ssh/{dart_context.ssh_key}' if dart_context.ssh_key is not None else ''
        user = dart_context.dart_env.default_env.user if dart_context.dart_env.default_env.user is not None else 'ubuntu'
        command = f'ssh {id_opt} -t {user}@{host} \'{cmd}\''

    print(command)
    os.system(command)
