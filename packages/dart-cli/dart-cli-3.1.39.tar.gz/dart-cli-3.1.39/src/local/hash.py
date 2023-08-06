import hashlib
import os
import shutil

import click


@click.command(name='hash')
@click.argument('files', nargs=-1, required=False)
@click.option('-i', '--input-dir', required=False, help='Get all files from the input directory (recursively)')
@click.option('-r', '--rename', is_flag=True, help='Rename files using doc-ids (preserves directory structure unless used with --output-dir')
@click.option('-o', '--output-dir', required=False, help='Optionally copy files to a separate directory (can only use in conjunction with --rename). Will not preserve directory structure.')
def hash_files(files, input_dir, rename, output_dir):
    """Generate out the doc id (MD5 hash) of one or more documents"""
    file_paths = []
    for file in files:
        file_paths.append(file)

    for root, subFolders, files in os.walk(input_dir):
        for filename in files:
            file_paths.append(os.path.join(root, filename))

    for file_path in file_paths:
        extension = os.path.splitext(file_path)[-1]
        try:
            with open(file_path, 'rb') as file:
                file_content = file.read()
                file_md5_hash = hashlib.md5(file_content).hexdigest()
            if rename:
                new_filename = file_md5_hash + extension
                if extension == '':
                    new_filename = file_md5_hash
                if output_dir is None:
                    # Get parent directory of file
                    dir_out = os.path.abspath(os.path.join(file_path, os.pardir))
                    shutil.move(file_path, os.path.join(dir_out, new_filename))
                else:
                    dir_out = output_dir
                    shutil.copy(file_path, os.path.join(dir_out, new_filename))
            else:
                print(file_md5_hash)
        except Exception:
            continue
