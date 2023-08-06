import json
import os
from pathlib import Path

import click
from dart_context.dart_context import DartContext

from cli import global_options
import requests
from time import sleep
from time import time
import queue
import threading
import shutil

from utilities.auth import generate_auth_headers
from utilities.url import get_base_url


class WorkerThread(threading.Thread):
    def __init__(self, files_queue, service_url: str, completed_file_path: str, failed_file_path: str, auth_headers: {}, metadata_obj: dict):
        threading.Thread.__init__(self)
        self.files_queue = files_queue
        self.service_url = service_url
        self.completed_file_path = completed_file_path
        self.failed_file_path = failed_file_path
        self.auth_headers = auth_headers
        self.metadata_obj = metadata_obj

    def run(self):
        while True:
            job_to_scan = self.files_queue.get()
            file_index = job_to_scan['index']
            file_path = job_to_scan['file_path']
            if file_index % 500 == 0:
                print(f'Posting: #{file_index} filename: {file_path.name}')
            doc_metadata = {}
            if 'meta_path' in job_to_scan:
                meta_path = job_to_scan['meta_path']
                if meta_path.is_file():
                    with open(meta_path, 'r', encoding='utf-8') as meta_file:
                        doc_metadata = json.loads(meta_file.read())
                        print(doc_metadata)

            if 'reannotate' in self.metadata_obj:
                doc_metadata['reannotate'] = self.metadata_obj['reannotate']

            if 'genre' in self.metadata_obj:
                doc_metadata['genre'] = self.metadata_obj['genre']

            if 'labels' in self.metadata_obj:
                if 'labels' not in doc_metadata:
                    doc_metadata['labels'] = self.metadata_obj['labels']
                else:
                    label_set = set(doc_metadata['labels'])
                    for label in self.metadata_obj['labels']:
                        label_set.add(label)
                    doc_metadata['labels'] = list(label_set)

            if 'tenants' in self.metadata_obj:
                if 'tenants' not in doc_metadata:
                    doc_metadata['tenants'] = self.metadata_obj['tenants']
                else:
                    label_set = set(doc_metadata['tenants'])
                    for label in self.metadata_obj['tenants']:
                        label_set.add(label)
                    doc_metadata['tenants'] = list(label_set)

            status, message = upload_file(file_path=file_path, service_url=self.service_url, auth_headers=self.auth_headers, metadata=json.dumps(doc_metadata))
            if status is True:
                move_file(file_path, self.completed_file_path)
            else:
                move_file(file_path, self.failed_file_path)
                print(f'failed: {status} message: {message}')
            self.files_queue.task_done()


def try_post(url, post_files, sleep_time, headers, numtimes):
    times_left = numtimes - 1
    try:
        response = requests.post(f"{url}", files=post_files, headers=headers)
        if response.status_code == 201 or response.status_code == 200:
            response.close()
            return [True, response.text]
        else:
            if times_left == 0:
                response.close()
                return [False, f"FAILED TO POST. Response status-code: {response.status_code}"]
            else:
                sleep(sleep_time)
                response.close()
                return try_post(url, post_files, sleep_time, headers, times_left)
    except Exception as e:
        print(f"Exception: {e}")
        if times_left == 0:
            return [False, f"FAILED TO POST. Exception: {str(e)}"]
        else:
            sleep(sleep_time)
            return try_post(url, post_files, sleep_time, headers, times_left)


def generate_files_queue(files, directory: str, ignore_meta):
    _files_dict = {}
    _files_queue = queue.Queue()
    index = 0

    def build_entry(file_path):
        basename = os.path.basename(file_path)
        file_path_path = Path(file_path)
        queue_entry = {'index': index, 'file_path': file_path_path}
        if not ignore_meta:
            meta_path = file_path_path.parent.joinpath(f"{basename.split('.')[0]}.meta")
            queue_entry['meta_path'] = meta_path
        return queue_entry

    if files is not None:
        for file_path in files:
            if os.path.isdir(file_path):
                continue
            basename = os.path.basename(file_path)
            if basename.startswith('.'):
                continue
            if basename.endswith('.meta'):
                continue

            _files_queue.put(build_entry(file_path))
            index += 1

    if directory is not None:
        for (root_dir, sub_dirs, files) in os.walk(directory):
            for file in files:
                basename = os.path.basename(file)
                if basename.startswith('.'):
                    continue
                if ignore_meta and basename.endswith('.meta'):
                    continue
                file_path = os.path.join(root_dir, file)
                _files_queue.put(build_entry(file_path))
                index += 1

    return _files_queue


def upload_file(file_path: str, service_url: str, auth_headers: {}, metadata: str):
    with open(file_path, 'rb') as file:
        post_files = {
            'file': (file.name, file),
            'metadata': (None, metadata, 'application/json')
        }
        return try_post(url=service_url, post_files=post_files, sleep_time=0.2, numtimes=1, headers=auth_headers)


def move_file(source_file_path: str, destination_file_path: str):
    if destination_file_path is not None:
        filename = os.path.basename(source_file_path)
        shutil.move(source_file_path, Path(destination_file_path).joinpath(filename))


def upload_raws(dart_context: DartContext, files, input_dir, failed_dir, succeeded_dir, metadata_obj, threads, ignore_meta_files):
    url = get_base_url('forklift', dart_context) + '/upload'
    auth_headers = generate_auth_headers(dart_context)

    # track time
    start_time = time()

    files_to_post_queue = generate_files_queue(files, input_dir, ignore_meta_files)

    for i in range(threads):
        worker = WorkerThread(files_to_post_queue, url, succeeded_dir, failed_dir, auth_headers, metadata_obj)
        worker.setDaemon(True)
        worker.start()

    files_to_post_queue.join()

    total_time = (time() - start_time) / 60
    print(f"Completed in {round(total_time, 2)} minutes")


@click.command(name='submit')
@global_options.dart_options
@click.option('-s', '--succeeded-dir', required=False, default=None)
@click.option('-f', '--failed-dir', required=False, default=None)
@click.option('--ignore-meta-files', required=False, is_flag = True, flag_value = True, default = False, help='Do not use files with extension ".meta" as per-file metadata of other docs with the same base name.')
@click.option('--metadata', required=False, default=None)
@click.option('--metadata-file', required=False, default=None)
@click.option('--label', required=False, default=None, multiple=True, help='Values should be separated by semicolons')
@click.option('--threads', required=False, default=6)
@click.option('--input-dir', required=False, default=None, help='Forklift all documents in a directory recursively')
@click.argument('files', required=False, nargs=-1)
@global_options.pass_dart_context
def submit_command(dart_context : DartContext,
                   files,
                   input_dir,
                   ignore_meta_files,
                   succeeded_dir,
                   failed_dir,
                   metadata,
                   metadata_file,
                   label,
                   threads):
    """Upload raw documents for processing"""

    if input_dir is None and len(files) == 0:
        raise click.exceptions.BadArgumentUsage('you must provide either input directory or files for upload')

    metadata_obj = {}
    if metadata_file is not None:
        with open(metadata_file) as metadata_file_ptr:
            metadata_obj.update(json.loads(metadata_file_ptr.read()))
    if metadata is not None:
        metadata_obj.update(json.loads(metadata))
    if label is not None:
        labels_list = list(label)
        metadata_obj['labels'] = labels_list
    if len(dart_context.tenants()) != 0:
        if 'tenants' in metadata_obj:
            metadata_obj['tenants'] = metadata_obj['tenants'] + dart_context.tenants()
        else:
            metadata_obj['tenants'] = dart_context.tenants()

    print(metadata_obj)
    upload_raws(dart_context, files, input_dir, failed_dir, succeeded_dir, metadata_obj, threads, ignore_meta_files)
