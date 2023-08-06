import click
import requests

from utilities.auth import generate_auth_headers
from utilities.url import get_base_url

from dart_context.dart_context import DartContext

from cli.global_options import dart_options, pass_dart_context


def add_tenant(context : DartContext, tenant):
    base_url = get_base_url('tenants', context)
    auth_headers = generate_auth_headers(context)
    res = requests.post(url=base_url + f'/{tenant}', headers=auth_headers)
    if res.status_code != 201:
        print(f"Unable to add {tenant} ({res.status_code}): {res.text}")
    else:
        print(f'Added: {tenant}')

@click.command(name='add')
@dart_options
@click.argument('tenants', required=True, nargs=-1)
@pass_dart_context
def add_command(context : DartContext, tenants):
    """Add one or more tenants"""
    for tenant in tenants:
        add_tenant(context, tenant)

@click.command(name='clone')
@dart_options
@click.argument('existing-tenant', required=True, nargs=1)
@click.argument('new-tenant', required=True, nargs=1)
@pass_dart_context
def clone_command(context : DartContext, existing_tenant, new_tenant):
    """Clone a tenant"""
    base_url = get_base_url('tenants', context)
    auth_headers = generate_auth_headers(context)
    res = requests.post(url=base_url + f'/{existing_tenant}/clone/{new_tenant}', headers=auth_headers)
    if res.status_code != 201:
        print(f"Unable to clone {existing_tenant} ({res.status_code}):\n{res.text}")
    else:
        print(f'Added: {new_tenant}')

