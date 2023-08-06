import click

from dart_context.dart_context import DartContext
from utilities.docker_utils import run_dart_docker_command


def deploy(dart_context: DartContext, ec2_ini_path):
    deploy_options = get_deploy_opts(dart_context, ec2_ini_path)
    return deploy_pipeline(dart_context, deploy_options)


def get_deploy_opts(dart_context: DartContext, ec2_ini_path):
    vm_username = dart_context.dart_env.tst_env.ssh_user
    vm_username_opt = '' if vm_username is None else f' --vm_username {vm_username}'
    ec2_ini_path_opt = '' if ec2_ini_path is None else f' --ec2_ini_path {ec2_ini_path}'
    if dart_context.dart_env.tst_env.env is None:
        raise Exception('missing DART environment: provide with --env or config profiles')
    if dart_context.docker_config.docker_username is None:
        raise Exception('missing docker username: provide with --docker-username or config profiles')
    if dart_context.docker_config.docker_password is None:
        raise Exception('missing docker password: provide with --docker-password or config profiles')
    if dart_context.aws_profile is None:
        raise Exception('missing AWS profiles: provide with --aws-profile or add to config')
    if dart_context.ssh_key is None:
        raise Exception('missing ssh key path : provide with --ssh-key or add to config')

    docker_registry_username_opt = f' --docker_registry_username {dart_context.docker_config.docker_username}'
    docker_registry_password_opt = f' --docker_registry_password {dart_context.docker_config.docker_password}'
    aws_profile_opt = f' --aws_profile {dart_context.aws_profile}'
    ssh_key_path_opt = f' --ssh_key_path /root/.ssh/{dart_context.ssh_key}'
    deploy_env_opt = f' --deploy_env {dart_context.dart_env.tst_env.env}'

    return vm_username_opt \
        + ec2_ini_path_opt \
        + docker_registry_password_opt \
        + docker_registry_username_opt \
        + aws_profile_opt \
        + ssh_key_path_opt \
        + deploy_env_opt


def deploy_pipeline(dart_context, deploy_options):
    return deploy_core_pipeline(dart_context, deploy_options)


def deploy_core_pipeline(dart_context, deploy_options):
    base_command = './start-dart-distributed.sh'
    command = base_command + deploy_options
    return run_dart_docker_command(dart_context, '/deployment/ansible', command)


def deploy_analytics(dart_context, deploy_options):
    base_command = './start-analytics.sh'
    command = base_command + deploy_options
    return run_dart_docker_command(dart_context, '/deployment/ansible', command)


def deploy_batch(dart_context, deploy_options):
    base_command = './start-batch.sh'
    command = base_command + deploy_options
    return run_dart_docker_command(dart_context, '/deployment/ansible', command)

def deploy_batch_master(dart_context, deploy_options):
    base_command = './start-batch-master.sh'
    command = base_command + deploy_options
    return run_dart_docker_command(dart_context, '/deployment/ansible', command)


def deploy_batch_workers(dart_context, deploy_options):
    base_command = './start-batch-workers.sh'
    command = base_command + deploy_options
    return run_dart_docker_command(dart_context, '/deployment/ansible', command)


def deploy_data(dart_context, deploy_options):
    if deploy_data_master(dart_context, deploy_options):
        return deploy_data_workers(dart_context, deploy_options)
    else:
        return False


def deploy_data_master(dart_context, deploy_options):
    base_command = './start-data-master.sh'
    command = base_command + deploy_options
    return run_dart_docker_command(dart_context, '/deployment/ansible', command)


def deploy_data_workers(dart_context, deploy_options):
    base_command = './start-data-workers.sh'
    command = base_command + deploy_options
    return run_dart_docker_command(dart_context, '/deployment/ansible', command)


def deploy_rest(dart_context, deploy_options):
    base_command = './start-rest.sh'
    command = base_command + deploy_options
    return run_dart_docker_command(dart_context, '/deployment/ansible', command)


def deploy_streaming(dart_context, deploy_options):
    base_command = './start-streaming.sh'
    command = base_command + deploy_options
    return run_dart_docker_command(dart_context, '/deployment/ansible', command)
