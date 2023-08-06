import json
import os
import re
import click
import requests

from utilities.auth import generate_auth_headers
from utilities.url import get_base_url

from cli.global_options import pass_dart_context, dart_options
from dart_context.dart_context import DartContext


def filter_metadata_fields(fields):
    regular_fields = set()
    metadata_fields = set()
    for field in fields:
        split_field = field.split('.')
        if len(split_field) > 1:
            [base_field, mfield] = split_field
            if base_field == 'extracted_metadata':
                metadata_fields.add(mfield)
        else:
            regular_fields.add(field)
    return regular_fields, metadata_fields


def process_cdr_data(cdr, incl, excl):
    (incl_regular, incl_metadata) = filter_metadata_fields(incl)
    (excl_regular, excl_metadata) = filter_metadata_fields(excl)

    cdr_fields = [field for field in cdr]
    for field in cdr_fields:
        if field == 'extracted_metadata':
            metadata_fields = [mfield for mfield in cdr['extracted_metadata']]
            for mfield in metadata_fields:
                if len(incl) != 0:
                    if mfield not in incl_metadata and 'extracted_metadata' not in incl_regular:
                        del cdr['extracted_metadata'][mfield]
                if mfield in cdr['extracted_metadata'] and mfield in excl_metadata:
                    del cdr['extracted_metadata'][mfield]
            if len(cdr['extracted_metadata']) == 0:
                del cdr['extracted_metadata']
        else:
            if len(incl) != 0:
                if field not in incl_regular:
                    del cdr[field]
            if field in cdr and field in excl_regular:
                del cdr[field]


@click.command(name='cdrs')
@dart_options
@click.option('-o', '--output', required=False, default=os.getcwd(), help='Directory to output files')
@click.option('-v/-s', '--view/--save', default=False, required=False, help='View file or save it (default save)')
@click.option('-e', '--ext', required=False, default='.cdr', help='Extension of cdr files')
@click.option('-i', '--include', required=False, multiple=True, default=[], help='Field to include in cdr')
@click.option('-x', '--exclude', required=False, multiple=True, default=[], help='Field to exclude from cdr')
@click.option('-f', '--ids-file', required=False, help='File with line-separated doc ids' )
@click.argument('doc-ids', required=False, nargs=-1)
@pass_dart_context
def get_cdrs(dart_context: DartContext, output, view, ext, include, exclude, ids_file, doc_ids):
    base_url = get_base_url('cdr-retrieval', dart_context)
    auth_headers = generate_auth_headers(dart_context)

    all_doc_ids = []
    if ids_file is not None:
        with open(ids_file, 'r') as f:
            for did in f:
                all_doc_ids.append(did)
    for did in doc_ids:
        all_doc_ids.append(did)

    if len(all_doc_ids) < 1:
        raise click.BadArgumentUsage('Must provide at least one document id')

    def url(doc_id):
        suffix = '' if len(dart_context.tenants()) < 1 else f'?tenant_id={dart_context.tenants()[0]}'
        return base_url + '/' + doc_id + suffix

    for doc_id in all_doc_ids:
        file_name = doc_id + '.' + ext.strip().lstrip('. ')
        file_path = os.path.join(output, file_name)
        with requests.get(url(doc_id), headers=auth_headers) as response:
            response.raise_for_status()
            ugly_json = response.text
            json_data = json.loads(ugly_json)
            process_cdr_data(json_data, include, exclude)
            if view:
                pretty_json = json.dumps(json_data, indent=4)
                print(pretty_json)
            else:
                with open(file_path, 'wb') as f:
                    f.write(json.dumps(json_data).encode('utf-8'))


def parse_content_disposition(header_value):
    return re.findall('filename=\"(.+)\"', header_value)[0]


@click.command(name='raws')
@dart_options
@click.option('-o', '--output', required=False, default=os.getcwd(), help='Directory to output files')
@click.option('-f', '--ids-file', required=False, help='File with line-separated doc ids' )
@click.argument('doc-ids', required=True, nargs=-1)
@pass_dart_context
def get_raws(dart_context: DartContext, output, ids_file, doc_ids):
    base_url  = get_base_url('cdr-retrieval', dart_context)
    auth_headers = generate_auth_headers(dart_context)

    all_doc_ids = []
    if ids_file is not None:
        with open(ids_file, 'r') as f:
            for did in f:
                all_doc_ids.append(did)
    for did in doc_ids:
        all_doc_ids.append(did)

    if len(all_doc_ids) < 1:
        raise click.BadArgumentUsage('Must provide at least one document id')

    def url(doc_id):
        suffix = '' if len(dart_context.tenants()) < 1 else f'?tenant_id={dart_context.tenants()[0]}'
        return base_url + '/raw/' + doc_id + suffix

    for doc_id in all_doc_ids:
        with requests.get(url(doc_id), stream=True, headers=auth_headers) as response:
            response.raise_for_status()
            content_disposition_header = response.headers['content-disposition']
            filename = parse_content_disposition(content_disposition_header)
            file_path = os.path.join(output, filename)
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    # if chunk:
                    f.write(chunk)
