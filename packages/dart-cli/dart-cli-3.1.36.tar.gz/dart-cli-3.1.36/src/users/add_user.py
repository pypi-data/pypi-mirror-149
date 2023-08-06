from pathlib import Path

import click
import requests
import json

from utilities.auth import generate_auth_headers
from utilities.url import get_base_url

from dart_context.dart_context import DartContext

from cli.global_options import dart_options, pass_dart_context


def merge_user_metadata(obj_a, obj_b):
    result = {**obj_a}
    if 'first_name' in obj_b:
        result['first_name'] = obj_b['first_name']
    if 'last_name' in obj_b:
        result['last_name'] = obj_b['last_name']
    if 'email' in obj_b:
        result['email'] = obj_b['email']
    if 'groups' in result and 'groups' in obj_b:
        result['groups'] = list(set(result['groups'] + set(obj_b['groups'])))
    elif 'groups' in obj_b:
        result['groups'] = obj_b['groups']
    return result


def generate_metadata(metadata_file, metadata, first_name, last_name, email, groups, password):
    metadata_obj = {}
    if metadata_file is not None and Path(metadata_file).is_file():
        with open(metadata_file, 'r') as m_file:
            metadata_obj = json.loads(m_file.read())
    if metadata is not None:
        metadata_obj = merge_user_metadata(metadata_obj, json.loads(metadata))
    if first_name is not None:
        metadata_obj['first_name'] = first_name
    if last_name is not None:
        metadata_obj['last_name'] = last_name
    if email is not None:
        metadata_obj['email'] = email
    if len(groups) > 0:
        if 'groups' in metadata_obj:
            metadata_obj['groups'] = list(set(metadata_obj['groups']) + set(groups))
        else:
            metadata_obj['groups'] = list(groups)
    if password is not None:
        metadata_obj['password'] = password
    return metadata_obj

@click.command(name='add')
@dart_options
@click.argument('user-name', required=True, nargs=1)
@click.option('--metadata-file', required=False)
@click.option('--metadata', required=False)
@click.option('--first-name', required=False)
@click.option('--last-name', required=False)
@click.option('--email', required=False)
@click.option('--group', required=False, default=None, multiple=True)
@click.option('--password', required=False, default=None )
@pass_dart_context
def add_command(context : DartContext, user_name, metadata_file, metadata, first_name, last_name, email, group, password):
    """Add a user"""
    metadata_obj = generate_metadata(metadata_file, metadata, first_name, last_name, email, group, password)
    base_url = get_base_url('users', context)
    auth_headers = generate_auth_headers(context)
    res = requests.post(url=base_url + f'/{user_name}', json=metadata_obj, headers=auth_headers)
    if res.status_code != 201:
        print(f"Unable to add {user_name} ({res.status_code}): {res.text}")
    else:
        print(f'Added: {user_name}')

@click.command(name='update')
@dart_options
@click.argument('user-name', required=True, nargs=1)
@click.option('--metadata-file', required=False)
@click.option('--metadata', required=False)
@click.option('--first-name', required=False)
@click.option('--last-name', required=False)
@click.option('--email', required=False)
@click.option('--group', required=False, default=None, multiple=True)
@click.option('--password', required=False, default=None )
@pass_dart_context
def update_command(context : DartContext, user_name, metadata_file, metadata, first_name, last_name, email, group, password):
    """Update a user"""
    metadata_obj = generate_metadata(metadata_file, metadata, first_name, last_name, email, group, password)
    base_url = get_base_url('users', context)
    auth_headers = generate_auth_headers(context)
    if not metadata_obj:
        raise click.exceptions.ClickException('Must provide updated data')
    res = requests.put(url=base_url + f'/{user_name}', json=metadata_obj, headers=auth_headers)
    if res.status_code != 200:
        print(f"Unable to update {user_name} ({res.status_code}): {res.text}")
    else:
        print(f'Updated: {user_name}')
