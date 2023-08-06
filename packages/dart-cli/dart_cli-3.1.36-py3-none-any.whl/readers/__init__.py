import click

from cli.global_options import dart_options, pass_dart_context


@click.group()
@dart_options
@pass_dart_context
def command(ctx):
    """Commands for interacting with readers output"""