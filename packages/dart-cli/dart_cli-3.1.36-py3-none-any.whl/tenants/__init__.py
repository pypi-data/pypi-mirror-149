import click

from cli.global_options import pass_dart_context, dart_options
from tenants import add_tenants, tenant_docs, ls_tenants, remove_tenants


@click.group(name='tenants')
@dart_options
@pass_dart_context
def command(ctx):
    """Commands for managing DART tenants"""

command.add_command(add_tenants.add_command)
command.add_command(add_tenants.clone_command)
command.add_command(tenant_docs.command)
command.add_command(ls_tenants.command)
command.add_command(remove_tenants.command)
