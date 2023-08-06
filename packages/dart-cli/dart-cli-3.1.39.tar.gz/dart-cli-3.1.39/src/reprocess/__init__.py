import click

from cli.global_options import dart_options, pass_dart_context
from reprocess.reprocess import reprocess_cdrs


@click.command(name='reprocess')
@dart_options
@click.option('-s', '--succeeded-dir', required=False, default=None)
@click.option('-f', '--failed-dir', required=False, default=None)
@click.option('--labels', required=False, default=None, help='Semicolon-separated string of labels to be added to '
                                                             'reprocessed cdrs')
@click.option('--threads', required=False, default=6)
@click.option('--input_dir', required=False, default=None, help='Forklift all documents in a directory recursively')
@click.argument('files', required=False, nargs=-1)
@pass_dart_context
def command(dart_context, succeeded_dir, failed_dir, labels, threads, input_dir, files):
    """Reprocess CDRs"""
    print(input_dir)
    print(files)
    if input_dir is None and len(files) == 0:
        raise click.exceptions.BadArgumentUsage('you must provide either input directory or files for reprocessing')
    reprocess_cdrs(dart_context, succeeded_dir, failed_dir, labels, threads, input_dir, files)
