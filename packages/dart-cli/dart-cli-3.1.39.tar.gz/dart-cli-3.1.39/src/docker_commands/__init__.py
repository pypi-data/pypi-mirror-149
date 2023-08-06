import click

from cli.global_options import dart_options, pass_dart_context
from docker_commands.docker_execs import open_debug, open_logs, open_psql


@click.command(name='psql')
@dart_options
@pass_dart_context
def psql_command(ctx):
    """Open a postgres session (requires psql and access to data-master)"""
    open_psql(ctx)

@click.command(name='debug', short_help='Exec into service container')
@dart_options
@click.argument('service', required=True, nargs=1)
@click.option('--instance', '-i', required=False, help="Manually specify instance (otherwise lookup instance from service definition)")
@pass_dart_context
def debug_command(ctx, service, instance):
    """Exec into service container

    Looks up container name and instance from services table, but you can use a container name for SERVICE and set
    the --instance option to manually select a docker container from an instance
    """
    open_debug(service, instance, ctx)

@click.command(name='logs', short_help='Display logs of service container')
@dart_options
@click.argument('service', required=True, nargs=1)
@click.option('--instance', '-i', required=False, help='Manually specify instance (otherwise lookup instance from service definition)')
@click.option('--follow', '-f', flag_value=True, default=False)
@pass_dart_context
def logs_command(ctx, service, instance, follow):
    """Display logs of service container

    Looks up container name and instance from services table, but you can use a container name for SERVICE and set
    the --instance option to manually select a docker container from an instance
    """
    open_logs(service, instance, follow, ctx)
