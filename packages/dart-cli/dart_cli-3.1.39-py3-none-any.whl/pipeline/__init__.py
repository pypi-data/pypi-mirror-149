import click

from cli.global_options import dart_options, pass_dart_context
from pipeline.commands import start_command, stop_command, destroy_command, provision_deploy_command, deploy_command, \
    provision_command, nuke_command, clean_command, info_command, refresh_command


@click.group(name='pipeline')
@dart_options
@pass_dart_context
def command(dart_context):
    """Commands for provisioning and deploying the DART pipeline"""

command.add_command(provision_command)
command.add_command(deploy_command)
command.add_command(provision_deploy_command)
command.add_command(refresh_command)
command.add_command(start_command)
command.add_command(stop_command)
command.add_command(info_command)
command.add_command(clean_command)
command.add_command(destroy_command)
command.add_command(nuke_command)
