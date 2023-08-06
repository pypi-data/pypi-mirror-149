import click

from cli.global_options import dart_options, pass_dart_context
from dart_context.dart_config import DartConfigException
from dart_context.dart_context import DartContext
from ssh.ssh import open_ssh


@click.command(name='ssh')
@dart_options
@click.argument('node', required=False)
@pass_dart_context
def command(ctx: DartContext, node):
    """Open a secure shell session with a DART node"""
    if ctx.dart_env.is_default():
        return open_ssh(ctx, '')

    if node is None:
        raise DartConfigException('"NODE" argument required for TST or custom deployment environments')

    open_ssh(ctx, node)
