import click

from cli import global_options
from health.dart_healthcheck import check_health


@click.command(name='health')
@global_options.dart_options
@click.option('--show-healthy/--hide-healthy',
              required=False,
              default=True,
              help='List all healthy services')
@click.option('--show-unhealthy/--hide-unhealthy',
              required=False,
              default=True,
              help='List all unhealthy services')
@click.argument('services',
                nargs=-1,
                required=False)
@global_options.pass_dart_context
def command(dart_context, show_healthy, show_unhealthy, services):
    """Check the status of DART services"""
    for service in services:
        healthy, msg = check_health(dart_context, service)
        if show_healthy and healthy:
            print(msg)
        if show_unhealthy and not healthy:
            print(msg)
