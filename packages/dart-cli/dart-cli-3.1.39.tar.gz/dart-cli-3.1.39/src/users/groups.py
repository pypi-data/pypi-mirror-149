import click
import requests

from utilities.auth import generate_auth_headers
from utilities.url import get_base_url

from dart_context.dart_context import DartContext

from cli.global_options import dart_options, pass_dart_context

@click.command(name='add-groups')
@dart_options
@click.argument('user-name', required=True, nargs=1)
@click.argument('groups', required=True, nargs=-1)
@pass_dart_context
def join_command(context : DartContext, user_name, groups):
    """Add a user to one or more groups"""
    base_url = get_base_url('users', context)
    auth_headers = generate_auth_headers(context)
    res = requests.post(url=base_url + f'/{user_name}/groups', json=groups, headers=auth_headers)
    if res.status_code != 200:
        print(f"Unable to update {user_name} ({res.status_code}): {res.text}")
    else:
        print(f'Updated: {user_name}')
