import os
import json
import click


def update_single_cdr(cdr_path, team, labels, replace_labels):
    try:
        with open(cdr_path, 'rt') as cdr_input_file:
            cdr_data = json.loads(cdr_input_file.read())

        if 'document_id' not in cdr_data:
            return

        if team is not None:
            cdr_data['team'] = team
        if replace_labels:
            cdr_data['labels'] = []
        if labels is not None:
            for label in labels:
                cdr_data['labels'].append(label)

        with open(cdr_path, 'wt') as cdr_output_file:
            cdr_text = json.dumps(cdr_data)
            cdr_output_file.write(cdr_text)

    except Exception as e:
        return


@click.command(name='update-cdrs')
@click.option('--team', required=False, multiple=True, help='Set new value of "team" field')
@click.option('--label', required=False, multiple=True, help='Add or replace labels. Use this option repeatedly to add multiple labels.')
@click.option('--replace-labels/--append-labels', required=False, default=False, help='Replace labels or add labels to existing labels. If --replace-labels is invoked without adding labels, labels will be cleared.')
@click.argument('cdrs-or-directories', required=True, nargs=-1)
def update_cdrs(team, label, replace_labels, cdrs_or_directories):
    """Update fields of CDRs in bulk"""
    for cdr_or_directory in cdrs_or_directories:
        if os.path.isdir(cdr_or_directory):
            for root, subFolders, files in os.walk(cdr_or_directory):
                for filename in files:
                    cdr_path = os.path.join(root, filename)
                    update_single_cdr(cdr_path, team, label, replace_labels)
        else:
            update_single_cdr(cdr_or_directory, team, label, replace_labels)
