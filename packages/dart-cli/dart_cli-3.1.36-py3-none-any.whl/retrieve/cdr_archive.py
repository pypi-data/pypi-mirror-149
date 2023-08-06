import os

import click
import requests

from utilities.auth import generate_auth_headers
from utilities.url import get_base_url

from dart_context.dart_context import DartContext

from cli.global_options import pass_dart_context, dart_options


@click.command(name='cdr-archive')
@dart_options
@click.option('-o', '--output', required=False)
@pass_dart_context
def get_cdr_archive(dart_context: DartContext, output):
    base_url = get_base_url('cdr-archive', dart_context)
    url = base_url + '/archive'
    output_path = output if output is not None else os.path.join(os.getcwd(), 'cdr-archive.zip')
    file_path = output_path
    if os.path.isdir(output_path):
        file_path = os.path.join(output, 'cdr-archive.zip')
    elif output_path.split('.')[-1] != 'zip':
        file_path = output_path + '.zip'

    auth_headers = generate_auth_headers(dart_context)

    with requests.get(url, stream=True, headers=auth_headers) as response:
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk:
                f.write(chunk)
