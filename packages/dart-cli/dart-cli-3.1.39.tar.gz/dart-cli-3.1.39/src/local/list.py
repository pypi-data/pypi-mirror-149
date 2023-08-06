import click
import os
import sys
import json
import shutil
import contextlib

@contextlib.contextmanager
def smart_open(filename=None):
    if filename and filename != '-':
        fh = open(filename, 'w')
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()

@click.command(name='list-ids')
@click.option('--input-dir', required=True)
@click.option('-o', '--output', required=False)
def list_ids(input_dir, output):
    """Lists doc ids of all CDRs in a directory (including subdirectories"""

    with smart_open(output) as file_out:
        for root, subFolders, files in os.walk(input_dir):
            for filename in files:
                try:
                    with open(os.path.join(root, filename), 'rt') as cdr_file:
                        cdr_data = json.loads(cdr_file.read())
                        doc_id = cdr_data['document_id']
                        print(doc_id, file=file_out)
                except Exception:
                    continue
