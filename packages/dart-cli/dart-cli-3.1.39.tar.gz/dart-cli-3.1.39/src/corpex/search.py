import click
import json

from dart_context.dart_context import DartContext

from cli.global_options import pass_dart_context, dart_options

from corpex.corpex_utilties import search, count


@click.command(name='search')
@dart_options
@click.option('-f', '--query-file', required=False)
@click.option('-q', '--query', required=False)
@click.option('--page-size', type=int, required=False, help='Override page size parameter')
@click.option('--page', type=int, required=False, help='Override page number parameter')
@click.option('-i', '--include', required=False, multiple=True, default=[], help='Override fields to include')
@pass_dart_context
def search_command(dart_context: DartContext, query_file, query, page_size, page, include):
    """Search for documents using corpex queries"""
    if query is not None and query_file is not None:
        raise click.exceptions.BadOptionUsage('query-file, query', 'Both options cannot be used together')
    elif query is None and query_file is None:
        corpex_query = {'queries': []}
    elif query is not None:
        corpex_query = json.loads(query)
    else:
        with open(query_file, 'rt') as qf:
            corpex_query = json.loads(qf.read())

    if page_size is not None:
        corpex_query['page_size'] = page_size
    if page is not None:
        corpex_query['page'] = page
    if len(include) > 0:
        corpex_query['fields'] = include

    print(dart_context.tenants())

    if len(dart_context.tenants()) > 0:
        corpex_query['tenant_id'] = dart_context.tenants()[0]

    print(json.dumps(search(dart_context, corpex_query), indent=4))


@click.command(name='count')
@dart_options
@click.option('-f', '--query-file', required=False)
@click.option('-q', '--query', required=False)
@pass_dart_context
def count_command(dart_context: DartContext, query_file, query):
    """Count documents using corpex queries"""
    if query is not None and query_file is not None:
        raise click.exceptions.BadOptionUsage('query-file, query', 'Both options cannot be used together')
    elif query is None and query_file is None:
        corpex_query = {'queries': []}
    elif query is not None:
        corpex_query = json.loads(query)
    else:
        with open(query_file, 'rt') as qf:
            corpex_query = json.loads(qf.read())

    if len(dart_context.tenants()) > 0:
        corpex_query['tenant_id'] = dart_context.tenants()[0]

    print(count(dart_context, corpex_query))
