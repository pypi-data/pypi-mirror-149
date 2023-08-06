import click

from cli.global_options import dart_options, pass_dart_context
from retrieve.cdr_archive import get_cdr_archive
from retrieve.cdr_retrieval import get_cdrs, get_raws


@click.group(name='retrieve')
@dart_options
@pass_dart_context
def command(ctx):
    """Commands for retrieving DART artifacts"""


command.add_command(get_cdr_archive)
command.add_command(get_cdrs)
command.add_command(get_raws)
