from dart_context.dart_context import DartContext
from pipeline.deploy import get_deploy_opts
from utilities.docker_utils import run_dart_docker_command


def get_opts(dart_context: DartContext, no_prompt):
    if dart_context.dart_env.tst_env.env is None:
        raise Exception('missing DART environment: provide with --env or config profiles')
    if dart_context.aws_profile is None:
        raise Exception('missing AWS profiles: provide with --aws-profiles or add to config')

    aws_profile_opt = f' --aws_profile {dart_context.aws_profile}'
    deploy_env_opt = f' --deploy_env {dart_context.dart_env.tst_env.env}'
    no_prompt_opt = '' if no_prompt is None or not no_prompt else f' --no_prompt'

    return aws_profile_opt \
        + deploy_env_opt \
        + no_prompt_opt

def clean_s3(dart_context, opts):
    base_command = './bin/clean-s3-environment.sh'
    command = base_command + opts
    return run_dart_docker_command(dart_context, '/deployment/dart_aws_infra', command)


def stop_containers_clear_data(dart_context, ec2_ini_path):
    opts = get_deploy_opts(dart_context, ec2_ini_path)
    base_command = './stop-dart-distributed.sh'
    command = base_command + opts
    return run_dart_docker_command(dart_context, '/deployment/ansible', command)

