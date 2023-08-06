from utilities.docker_utils import run_dart_docker_command

from dart_context.dart_context import DartContext


def destroy(dart_context):
    provision_opts = get_destroy_opts(dart_context)
    return destroy_all(dart_context, provision_opts)


def provision(dart_context):
    provision_opts = get_provision_opts(dart_context)
    return provision_core(dart_context, provision_opts)


def get_provision_opts(dart_context: DartContext):
    if dart_context.dart_env.tst_env.env is None:
        raise Exception('missing DART environment: provide with --env or add to config profile')
    if dart_context.aws_profile is None:
        raise Exception('missing AWS profile: provide with --aws-profiles or add to config profile')

    aws_profile_opt = f' --aws_profile {dart_context.aws_profile}'
    deploy_env_opt = f' --deploy_env {dart_context.dart_env.tst_env.env}'
    deploy_profile_opt = '' if dart_context.dart_env.tst_env.deploy_profile is None else f' --deploy_profile {dart_context.dart_env.tst_env.deploy_profile}'
    aws_environment_opt = '' if dart_context.dart_env.tst_env.aws_environment is None else f' --aws_environment {dart_context.dart_env.tst_env.aws_environment}'

    return aws_profile_opt \
           + deploy_env_opt \
           + deploy_env_opt \
           + deploy_profile_opt \
           + aws_environment_opt


def get_destroy_opts(dart_context: DartContext):
    if dart_context.dart_env.tst_env.env is None:
        raise Exception('missing DART environment: provide with --env or config profiles')
    if dart_context.aws_profile is None:
        raise Exception('missing AWS profiles: provide with --aws-profiles or add to config')

    aws_profile_opt = f' --aws_profile {dart_context.aws_profile}'
    deploy_env_opt = f' --deploy_env {dart_context.dart_env.tst_env.env}'
    aws_environment_opt = '' if dart_context.dart_env.tst_env.aws_environment is None else f' --aws_environment {dart_context.dart_env.tst_env.aws_environment}'

    return aws_profile_opt \
           + deploy_env_opt \
           + aws_environment_opt


def provision_core(dart_context, provision_opts):
    base_command = './provision-dart-distributed.sh'
    command = base_command + provision_opts
    return run_dart_docker_command(dart_context, '/deployment/dart_aws_infra', command)


def destroy_all(dart_context, provision_opts):
    base_command = './destroy-dart-distributed.sh'
    command = base_command + provision_opts
    return run_dart_docker_command(dart_context, '/deployment/dart_aws_infra', command)


def provision_batch(dart_context, provision_opts):
    base_command = './provision-batch.sh'
    command = base_command + provision_opts
    return run_dart_docker_command(dart_context, '/deployment/dart_aws_infra', command)


def destroy_batch(dart_context, provision_opts):
    base_command = './destroy-batch.sh'
    command = base_command + provision_opts
    return run_dart_docker_command(dart_context, '/deployment/dart_aws_infra', command)


def provision_pipeline(dart_context, provision_opts):
    base_command = './provision-dart-distributed.sh'
    command = base_command + provision_opts
    return run_dart_docker_command(dart_context, '/deployment/dart_aws_infra', command)


def destroy_core_pipeline(dart_context, provision_opts):
    base_command = './destroy-dart-distributed.sh'
    command = base_command + provision_opts
    return run_dart_docker_command(dart_context, '/deployment/dart_aws_infra', command)

def start_pipeline(dart_context : DartContext):
    base_command = './start-environment.sh'
    command = base_command  + f' --deploy_env {dart_context.dart_env.tst_env.env} --aws_profile {dart_context.aws_profile}'
    return run_dart_docker_command(dart_context, '/deployment/dart_aws_infra/bin', command)

def stop_pipeline(dart_context : DartContext):
    base_command = './stop-environment.sh'
    command = base_command  + f' --deploy_env {dart_context.dart_env.tst_env.env} --aws_profile {dart_context.aws_profile}'
    return run_dart_docker_command(dart_context, '/deployment/dart_aws_infra/bin', command)

def info_pipeline(dart_context : DartContext):
    base_command = './info-environment.sh'
    command = base_command  + f' --deploy_env {dart_context.dart_env.tst_env.env} --aws_profile {dart_context.aws_profile}'
    return run_dart_docker_command(dart_context, '/deployment/dart_aws_infra/bin', command)