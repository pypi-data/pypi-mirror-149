import docker
import click
from pathlib import Path
from docker.errors import ContainerError
import dockerpty

from dart_context.dart_config import MissingParameterException
from dart_context.dart_context import DartContext


def get_docker_client(dart_context: DartContext):
    client: docker.DockerClient = docker.client.from_env()
    if dart_context.docker_config.docker_password is not None and dart_context.docker_config.docker_username is not None:
        print('Logging into docker')
        registry_host = dart_context.docker_config.docker_registry_host
        client.login(username=dart_context.docker_config.docker_username,
                     password=dart_context.docker_config.docker_password,
                     registry=registry_host)

    return client


def get_dart_image(dart_context: DartContext):
    if dart_context.dart_env.tst_env.project_id is None or dart_context.dart_env.tst_env.pipeline_version is None:
        raise MissingParameterException('dart-version (including project-id and pipeline-version)')

    image_prefix = f'{dart_context.docker_config.docker_registry_host}/{dart_context.docker_config.docker_namespace}/'
    wm_image = 'wm-dart-pipeline'
    dev_image = 'dev-dart-pipeline'
    if dart_context.dart_env.tst_env.project_id == 'wm':
        image = wm_image
    elif dart_context.dart_env.tst_env.project_id == 'dev':
        image = dev_image
    else:
        raise click.BadOptionUsage('dart-version', 'Allowed values for project-id are wm|dev')

    return image_prefix + image + ':' + dart_context.dart_env.tst_env.pipeline_version


def run_dart_docker_command(dart_context: DartContext, working_dir, command):
    client: docker.DockerClient = get_docker_client(dart_context)

    # Image
    image_url = get_dart_image(dart_context)

    # Volumes
    home = Path.home()
    aws_path = str(home.joinpath('.aws'))
    ssh_path = str(home.joinpath('.ssh'))
    volumes = {
        aws_path: {'bind': '/root/.aws', 'mode': 'ro'},
        ssh_path: {'bind': '/root/.ssh', 'mode': 'ro'},
    }

    return_status = True

    print(f'DOCKER RUN')
    print(f'==========')
    print(f'image:   {image_url}')
    print(f'workdir: {working_dir}')
    print(f'command: {command}')
    print(f'volumes: {volumes}')
    # Run container
    try:
        image = client.images.pull(image_url)
        container = client.api.create_container(
            host_config=client.api.create_host_config(binds=volumes),
            volumes=['/root/.aws', '/root/.ssh'],
            image=image_url,
            command=command,
            # entrypoint='/bin/bash',
            stdin_open=True,
            tty=True,
            working_dir=working_dir)
        dockerpty.start(client.api, container)
        exit_status = client.api.wait(container)
        print(exit_status)
        if exit_status['StatusCode'] != 0:
            return_status = False
    except ContainerError as e:
        print(str(e))
        print(f'Task failed with status: {e.exit_status}')
        return_status = False

    return return_status
