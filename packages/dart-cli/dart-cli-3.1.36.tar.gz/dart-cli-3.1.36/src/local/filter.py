import hashlib

import click
import os
import json
import shutil

@click.command(name='filter-cdrs')
@click.option('--doc-ids-file', required=False)
@click.option('--team', required=False, multiple=True, help='Move/copy docs based on team field. Can use this flag repeatedly to filter multiple values (will move/copy any of them)')
@click.option('--label', required=False, multiple=True, help='Move/copy docs based on labels field. Can use this flag repeatedly to filter multiple values (use --all-labels/--any-labels to choose whether to filter all values or any)')
@click.option('--all-labels/--any-labels', default=False, help='Determine whether to require all labels or any')
@click.option('--input-dir', required=True)
@click.option('--output-dir', required=True)
@click.option('--move', default=False, required=False, help='If set, it will move files instead of copying them')
def cdr_filter(doc_ids_file, team, label, all_labels, input_dir, output_dir, move):
    """Copies or moves CDR documents from one directory to another based on a list of doc ids, labels, or team"""
    use_doc_ids = doc_ids_file is not None
    doc_id_set = set()
    if use_doc_ids:
        with open(doc_ids_file, 'rt') as doc_ids_file:
            for doc_id in doc_ids_file:
                doc_id_set.add(doc_id.strip())

    total_move_count = 0
    total_file_count = 0
    total_cdr_count = 0
    total_non_cdr_count = 0
    for root, subFolders, files in os.walk(input_dir):
        for filename in files:
            total_file_count += 1
            try:
                with open(os.path.join(root, filename), 'rt') as cdr_file:
                    cdr_data = json.loads(cdr_file.read())
                    doc_id = cdr_data['document_id']
                    total_cdr_count += 1
                    if use_doc_ids:
                        if cdr_data['document_id'] not in doc_id_set:
                            continue
                    if team is not None and len(team) > 0:
                        break_out = True
                        for t in team:
                            if cdr_data['team'] == t:
                                break_out = False
                        if break_out:
                            continue
                    if label is not None and len(label) > 0:
                        break_out = not all_labels
                        for l in label:
                            if all_labels:
                                if l not in cdr_data['labels']:
                                    break_out = True
                            else:
                                if l in cdr_data['labels']:
                                    break_out = False
                        if break_out:
                            continue
                if move:
                    shutil.move(os.path.join(root, filename), os.path.join(output_dir, filename))
                else:
                    shutil.copyfile(os.path.join(root, filename), os.path.join(output_dir, filename))
                total_move_count += 1
            except Exception:
                total_non_cdr_count += 1
                continue

    print(f'{"Moved" if move else "Copied"} {total_move_count} documents out of {total_cdr_count} CDRs found among {total_file_count} files')

@click.command(name='filter-docs')
@click.option('--doc-ids-file', required=True)
@click.option('-h', '--use-hash', required=False, is_flag=True, default=False, help='Use MD5 hash rather than filename for filtering')
@click.option('-r', '--rename', required=False, is_flag=True, default=False, help='Rename to doc-id using MD5 hash')
@click.option('-i', '--input-dir', required=True)
@click.option('-o', '--output-dir', required=True)
@click.option('--ext', default=[], multiple=True, required=False, help='Only select files with a given extension. (Can be used multiple times to include multiple extensions.)')
@click.option('--no-ext', default=[], multiple=True, required=False, help='Ignore files with a given extension. (Can be used multiple times to exclude multiple extensions.)')
@click.option('--move/--copy', default=False, required=False, help='Move or copy files from input-dir to output-dir (default copy)')
def raw_filter(doc_ids_file, use_hash, rename, input_dir, output_dir, ext, no_ext, move):
    """Copies or moves documents named by doc id from one directory to another based on a list of doc ids"""
    doc_id_set = set()
    with open(doc_ids_file, 'rt') as doc_ids_file:
        for doc_id in doc_ids_file:
            doc_id_set.add(doc_id.strip())
    total_id_count = len(doc_id_set)
    total_filtered_count = 0
    total_found_count = 0

    incl_ext_set = set(ext)
    excl_ext_set = set(no_ext)

    if len(incl_ext_set) > 0 and len(excl_ext_set) > 0:
        raise click.BadOptionUsage('ext', '--ext and --no-ext cannot be used together')

    for root, subFolders, files in os.walk(input_dir):
        for filename in files:
            total_found_count += 1
            [root_name, extension] = os.path.splitext(filename)
            if (len(incl_ext_set) > 0 and extension not in incl_ext_set) or extension in excl_ext_set:
                # print(f'{extension} is not in {incl_ext_set} or is in {excl_ext_set}')
                continue
            file_id = root_name
            if use_hash:
                with open(os.path.join(root, filename), 'rb') as file:
                    file_content = file.read()
                    file_id = hashlib.md5(file_content).hexdigest()
            if file_id in doc_id_set:
                new_filename = filename
                if rename and extension is not None:
                    new_filename = file_id + extension
                elif rename:
                    new_filename = file_id

                if move:
                    shutil.move(os.path.join(root, filename), os.path.join(output_dir, new_filename))
                else:
                    shutil.copyfile(os.path.join(root, filename), os.path.join(output_dir, new_filename))
                total_filtered_count += 1

    action = 'Moved'
    if not move:
        action = 'Copied'

    print(f'{action} {total_filtered_count} documents out of {total_id_count} indexed and {total_found_count} found')
