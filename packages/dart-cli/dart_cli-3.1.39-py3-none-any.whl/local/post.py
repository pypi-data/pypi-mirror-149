import json

import os
from pathlib import Path

import click

import requests
from time import sleep
from time import time
import queue
import threading
import shutil


class WorkerThread(threading.Thread):
    def __init__(self, files_queue, service_url: str, completed_file_path: str, failed_file_path: str, auth_headers: {},
                 upload_format: str):
        threading.Thread.__init__(self)
        self.files_queue = files_queue
        self.service_url = service_url
        self.completed_file_path = completed_file_path
        self.failed_file_path = failed_file_path
        self.auth_headers = auth_headers
        self.upload_format = upload_format

    def run(self):
        while True:
            job_to_scan = self.files_queue.get()
            file_index = job_to_scan['index']
            file_path = job_to_scan['file_path']
            if file_index % 500 == 0:
                print(f'Posting: #{file_index} filename: {file_path.name}')
            status, message = upload_file(file_path=file_path, service_url=self.service_url,
                                          auth_headers=self.auth_headers, upload_format=self.upload_format)
            if status is True:
                move_file(file_path, self.completed_file_path)
            else:
                move_file(file_path, self.failed_file_path)
                print(f'failed: {status} message: {message}')
            self.files_queue.task_done()


def try_post(url, post_files=None, json_data=None, sleep_time=None, headers=None, numtimes=None):
    times_left = numtimes - 1
    try:
        response = requests.post(f"{url}", files=post_files, json=json_data, headers=headers)
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
                return try_post(url, post_files, json_data, sleep_time, headers, times_left)
    except Exception as e:
        print(f"Exception: {e}")
        if times_left == 0:
            return [False, f"FAILED TO POST. Exception: {str(e)}"]
        else:
            sleep(sleep_time)
            return try_post(url, post_files, json_data, sleep_time, headers, times_left)


def generate_files_queue(files, directory: str):
    _files_queue = queue.Queue()
    index = 0

    if files is not None:
        for file_path in files:
            if os.path.isdir(file_path):
                continue

            os.path.basename(file_path)
            if os.path.basename(file_path).startswith('.'):
                continue
            _files_queue.put({'index': index, 'file_path': Path(file_path)})
            index += 1

    if directory is not None:
        for (root_dir, sub_dirs, files) in os.walk(directory):
            for file in files:
                if file.startswith('.'):
                    continue
                _files_queue.put({'index': index, 'file_path': Path(root_dir).joinpath(file)})
                index += 1

    return _files_queue


def upload_file(file_path: str, service_url: str, auth_headers: {}, upload_format: str):
    with open(file_path, 'rb') as file:
        if upload_format == 'file':
            post_files = {
                'file': (file.name, file),
            }
            return try_post(url=service_url, post_files=post_files, sleep_time=0.2, numtimes=1, headers=auth_headers)
        if upload_format == 'json':
            json_data = json.loads(file.read().decode('utf8'))
            return try_post(url=service_url, json_data=json_data, sleep_time=0.2, numtimes=1, headers=auth_headers)


def move_file(source_file_path: str, destination_file_path: str):
    if destination_file_path is not None:
        filename = os.path.basename(source_file_path)
        shutil.move(source_file_path, Path(destination_file_path).joinpath(filename))


def upload(url, files, input_dir, failed_dir, succeeded_dir, upload_format, auth_headers_in, threads):
    # track time
    start_time = time()

    files_to_post_queue = generate_files_queue(files, input_dir)

    for i in range(threads):
        worker = WorkerThread(files_to_post_queue, url, succeeded_dir, failed_dir, auth_headers_in, upload_format)
        worker.setDaemon(True)
        worker.start()

    files_to_post_queue.join()

    total_time = (time() - start_time) / 60
    print(f"Completed in {round(total_time, 2)} minutes")


@click.command(name='post')
@click.option('--url', required=True)
@click.option('--threads', required=False, default=6)
@click.option('-u', '--upload-format', type=click.Choice(['json', 'binary', 'text'], case_sensitive=False),
              default='json')
@click.option('--input-dir', required=False, default=None, help='Forklift all documents in a directory recursively')
@click.option('-s', '--succeeded-dir', required=False, default=None)
@click.option('-f', '--failed-dir', required=False, default=None)
@click.option('-a', '--auth', required=False, default=None, help='Basic auth: [username]:[password]')
@click.argument('files', required=False, nargs=-1)
def post_command(url, threads, upload_format, input_dir, succeeded_dir, failed_dir, auth, files):
    """Post files to a service"""
    if input_dir is None and len(files) == 0:
        raise click.exceptions.BadArgumentUsage('you must provide either input directory or files for upload')
    upload(url, files, input_dir, failed_dir, succeeded_dir, upload_format, auth, threads)
