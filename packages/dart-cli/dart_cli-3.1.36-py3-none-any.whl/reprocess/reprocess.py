
#!/usr/bin/env python3

import os.path
from pathlib import Path
import json
import shutil

import requests
from dart_context.dart_context import DartContext

from utilities.auth import generate_auth_headers
from utilities.url import get_base_url


def transfer_file(source_file_path: str, destination_file_path: str):
    if destination_file_path is not None:
        filename = os.path.basename(source_file_path)
        shutil.move(source_file_path, Path(destination_file_path).joinpath(filename))

def upload_document(dart_context: DartContext, json, labels):
    url = get_base_url('reprocess', dart_context)
    cdr = json.loads(json)
    if labels is not None:
        if 'labels' in cdr:
            cdr['labels'].extend(labels)
        else:
            cdr['labels'] = labels

    auth_headers = generate_auth_headers(dart_context)
    response = requests.post(url, json=cdr, headers=auth_headers)

    if response.status_code < 300:
        return True
    else:
        print(f'Unable to reprocess cdr: {response.text}')
        return False

def reprocess_cdrs(dart_context, succeeded_dir, failed_dir, labels, threads, input_dir, files):
    if files is not None:
        for file_path in files:
            with open(file_path, 'rt') as file:
                file_json = json.loads(file.read())
            result = upload_document(dart_context, file_json, labels)
            if result:
                transfer_file(file_path, succeeded_dir)
            else:
                transfer_file(file_path, failed_dir)

    if input_dir is not None:
        for root, subFolders, files in os.walk(input_dir):
            for filename in files:
                if filename[-4:] != '.cdr' and filename[-5:] != '.json':
                    print(f"Not a cdr: {filename}")
                    continue

                file_path = Path(root).joinpath(filename)
                file = open(file_path, "r")
                file_json = json.loads(file.read())
                file.close()

                result = upload_document(dart_context, file_json, labels)
                if result:
                    transfer_file(file_path, succeeded_dir)
                else:
                    transfer_file(file_path, failed_dir)

