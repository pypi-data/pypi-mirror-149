import click
import requests

from utilities.auth import generate_auth_headers
from utilities.url import get_base_url

from dart_context.dart_context import DartContext

from cli.global_options import dart_options, pass_dart_context


@click.command(name='ls')
@dart_options
@pass_dart_context
def command(context: DartContext):
    """Display all tenants"""
    base_url  = get_base_url('tenants', context)
    auth_headers = generate_auth_headers(context)
    res = requests.get(url=base_url, headers=auth_headers)
    if res.status_code != 200:
        print(f"Unable to retrieve tenants:")
        print(f"Status: {res.status_code}")
        print(res.text)
    else:
        for tenant in res.json():
            print(tenant)
