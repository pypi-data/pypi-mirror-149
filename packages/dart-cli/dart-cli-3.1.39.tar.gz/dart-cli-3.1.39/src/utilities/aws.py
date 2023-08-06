import json

import boto3

from dart_context.dart_config import MissingParameterException, DartConfigException
from dart_context.dart_context import DartContext


def get_client(dart_context: DartContext, service: str):
    if dart_context.aws_profile is None:
        raise MissingParameterException('aws-profile')

    boto3.setup_default_session(profile_name=dart_context.aws_profile)
    return boto3.client(service)

def get_stack_name(dart_context: DartContext):
    if dart_context.dart_env.tst_env.env is None:
        raise MissingParameterException('env')

    return dart_context.dart_env.tst_env.env + '-base-resources'

def query_metadata(dart_context: DartContext):
    client = get_client(dart_context, 'cloudformation')
    stack_name = get_stack_name(dart_context)
    response = client.describe_stacks(StackName=stack_name)
    outputs = response['Stacks'][0]['Outputs']
    output_metadata = {}
    for output in outputs:
        if output['OutputKey'] == 'deploymetadata':
            output_metadata = json.loads(output['OutputValue'])
            break

    if 'app_version' not in output_metadata:
        raise DartConfigException('unable to retrieve pipeline-version from env metadata')
    if 'project_id' not in output_metadata:
        raise DartConfigException('unable to retrieve project-id from env metadata')
    if 'deploy_profile' not in output_metadata:
        raise DartConfigException('unable to retrieve deploy-profile from env metadata')

    dart_context.dart_env.tst_env.set_pipeline_version(output_metadata['app_version'])
    dart_context.dart_env.tst_env.set_project_id(output_metadata['project_id'].lower())
    dart_context.dart_env.tst_env.set_deploy_profile(output_metadata['deploy_profile'].lower())
