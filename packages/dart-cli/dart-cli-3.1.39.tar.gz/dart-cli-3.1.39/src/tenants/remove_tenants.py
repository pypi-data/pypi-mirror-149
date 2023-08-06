import click
import requests

from utilities.auth import generate_auth_headers
from utilities.url import get_base_url

from dart_context.dart_context import DartContext

from cli.global_options import dart_options, pass_dart_context


def remove_tenant(context : DartContext, tenant):
    base_url = get_base_url('tenants', context)
    auth_headers = generate_auth_headers(context)
    res = requests.delete(url=base_url + f'/{tenant}', headers=auth_headers)
    if res.status_code != 200:
        print(f"Unable to remove {tenant} ({res.status_code}): {res.text}")
    else:
        print(f'Removed: {tenant}')

@click.command(name='rm')
@dart_options
@click.argument('tenants', required=True, nargs=-1)
@pass_dart_context
def command(context : DartContext, tenants):
    """Remove one or more tenants"""
    for tenant in tenants:
        remove_tenant(context, tenant)

