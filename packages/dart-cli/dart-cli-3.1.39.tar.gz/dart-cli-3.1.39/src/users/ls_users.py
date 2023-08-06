import click
import requests

from utilities.auth import generate_auth_headers
from utilities.url import get_base_url

from dart_context.dart_context import DartContext

from cli.global_options import dart_options, pass_dart_context


def display_user(user_obj: {}):
    divider = ''.join('=' * (len(user_obj["user_name"]) + 6))
    print(f'User: {user_obj["user_name"]}\n{divider}')
    first_name = user_obj["first_name"] + ' ' if 'first_name' in user_obj else ''
    last_name = user_obj['last_name'] if 'last_name' in user_obj else ''
    full_name = first_name + last_name
    if len(full_name) > 0:
        print(f'Name: {full_name}')
    if 'email' in user_obj:
        print(f'Email: {user_obj["email"]}')
    if 'groups' in user_obj:
        print(f'Groups: {"; ".join(user_obj["groups"])}')
    print("")

@click.command(name='ls')
@dart_options
@click.option('--view', required=False, is_flag=True, flag_value=True, default=False)
@pass_dart_context
def ls_command(context : DartContext, view):
    """Display all users"""
    base_url  = get_base_url('users', context)
    auth_headers = generate_auth_headers(context)
    res = requests.get(url=base_url, headers=auth_headers)
    if res.status_code != 200:
        print(f"Unable to retrieve users:")
        print(f"Status: {res.status_code}")
        print(res.text)
    else:
        for user in res.json():
            if view:
                display_user(user)
            else:
                print(user['user_name'])

def get_user(context, user):
    base_url = get_base_url('users', context)
    auth_headers = generate_auth_headers(context)
    res = requests.get(url=base_url + f'/{user}', headers=auth_headers)
    if res.status_code != 200:
        print(f"Unable to retrieve users:")
        print(f"Status: {res.status_code}")
        print(res.text)
        return None
    else:
        return res.json()

@click.command(name='view')
@dart_options
@click.argument('users', required=True, nargs=-1)
@pass_dart_context
def view_command(context : DartContext, users):
    """Display all users"""
    for user in users:
        user_obj = get_user(context, user)
        if user_obj is not None:
            display_user(user_obj)
