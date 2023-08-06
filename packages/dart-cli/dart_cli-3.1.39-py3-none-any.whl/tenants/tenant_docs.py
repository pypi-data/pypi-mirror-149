import click
import requests

from utilities.auth import generate_auth_headers
from utilities.url import get_base_url

from dart_context.dart_context import DartContext

from cli.global_options import dart_options, pass_dart_context

@click.command(name='ls')
@dart_options
@click.argument('tenant-id', required=True, nargs=1)
@pass_dart_context
def ls_command(context: DartContext, tenant_id):
    """Display docs belonging to a tenant"""
    base_url = get_base_url('tenants', context)
    auth_headers = generate_auth_headers(context)
    print(base_url)
    res = requests.get(url=base_url + f'/{tenant_id}/documents', headers=auth_headers)
    if res.status_code != 200:
        print(f"Unable to retrieve documents from {tenant_id}:")
        print(f"Status: {res.status_code}")
        print(res.text)
    else:
        for doc in res.json():
            print(doc)

def get_doc_ids_list(doc_ids, doc_ids_file):
    doc_ids_set = set()
    if doc_ids_file is not None:
        with open(doc_ids_file, 'r') as didf:
            for line in didf:
                trimmed_line = line.strip()
                if len(trimmed_line) == 32:
                    doc_ids_set.add(trimmed_line)
    for did in doc_ids:
        doc_ids_set.add(did)

    return list(doc_ids_set)

@click.command(name='add')
@dart_options
@click.argument('tenant-id', required=True, nargs=1)
@click.argument('doc-ids', required=False, nargs=-1)
@click.option('--doc-ids-file', required=False)
@pass_dart_context
def add_command(context : DartContext, tenant_id, doc_ids, doc_ids_file):
    """Add docs to a tenant"""
    base_url  = get_base_url('tenants', context)
    auth_headers = generate_auth_headers(context)
    all_doc_ids = get_doc_ids_list(doc_ids, doc_ids_file)
    if len(all_doc_ids) < 1:
        print("Provide at least one document id to add")
        return
    doc_ids_log = f'{len(all_doc_ids)} documents' if len(all_doc_ids) > 10 else ", ".join(all_doc_ids)
    res = requests.post(
        url=base_url + f'/{tenant_id}/documents',
        json=all_doc_ids,
        headers=auth_headers,
    )
    if res.status_code != 200:
        print(f"Unable to add {doc_ids_log} to {tenant_id}:")
        print(f"Status: {res.status_code}")
        print(res.text)
    else:
        print(f'Added {doc_ids_log} to {tenant_id}')

@click.command(name='rm')
@dart_options
@click.argument('tenant-id', required=True, nargs=1)
@click.argument('doc-ids', required=False, nargs=-1)
@click.option('--doc-ids-file', required=False)
@pass_dart_context
def remove_command(context : DartContext, tenant_id, doc_ids, doc_ids_file):
    """Remove docs from a tenant"""
    base_url  = get_base_url('tenants', context)
    auth_headers = generate_auth_headers(context)
    all_doc_ids = get_doc_ids_list(doc_ids, doc_ids_file)
    if len(all_doc_ids) < 1:
        print("Provide at least one document id to remove")
        return
    doc_ids_log = f'{len(all_doc_ids)} documents' if len(all_doc_ids) > 10 else ", ".join(all_doc_ids)
    res = requests.post(
        url=base_url + f'/{tenant_id}/documents/remove',
        json=all_doc_ids,
        headers=auth_headers,
    )
    if res.status_code != 200:
        print(f"Unable to remove {doc_ids_log} from {tenant_id}:")
        print(f"Status: {res.status_code}")
        print(res.text)
    else:
        print(f'Removed {doc_ids_log} from {tenant_id}')

@click.group(name='docs')
@dart_options
@pass_dart_context
def command(context : DartContext):
    """Manage documents in a tenant"""

command.add_command(ls_command)
command.add_command(add_command)
command.add_command(remove_command)
