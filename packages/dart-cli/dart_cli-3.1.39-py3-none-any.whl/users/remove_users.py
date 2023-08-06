import click
import requests

from utilities.auth import generate_auth_headers
from utilities.url import get_base_url

from dart_context.dart_context import DartContext

from cli.global_options import dart_options, pass_dart_context


def remove_user(context : DartContext, user):
    base_url = get_base_url('users', context)
    auth_headers = generate_auth_headers(context)
    res = requests.delete(url=base_url + f'/{user}', headers=auth_headers)
    if res.status_code != 200:
        print(f"Unable to remove {user} ({res.status_code}): {res.text}")
    else:
        print(f'Removed: {user}')

@click.command(name='rm')
@dart_options
@click.argument('users', required=True, nargs=-1)
@pass_dart_context
def command(context : DartContext, users):
    """Remove one or more users"""
    for user in users:
        remove_user(context, user)

