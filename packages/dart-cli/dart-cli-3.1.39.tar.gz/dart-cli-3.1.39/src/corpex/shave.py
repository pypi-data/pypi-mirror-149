import click
import json

from cli.global_options import pass_dart_context, dart_options

from corpex.corpex_utilties import start_scroll, continue_scroll, shave


@click.command(name='shave')
@dart_options
@click.option('-f', '--query-file', required=False)
@click.option('-q', '--query', required=False)
@click.option('--corpex/--elasticsearch', required=False, default=True, help='Is the query meant for corpex or for elasticsearch. (Default corpex)')
@click.argument('count', required=True)
@pass_dart_context
def command(dart_context, query_file, query, corpex, count):
    """Shave documents using corpex or elasticsearch queries"""
    if query is not None and query_file is not None:
        raise click.exceptions.BadOptionUsage('query-file, query', 'Both options cannot be used together')
    elif query is None and query_file is None:
        raise click.exceptions.MissingParameter('You must pass a query string (--query) or a query file (--query-file)')
    elif query is not None:
        if corpex:
            shave(dart_context, json.loads(query), count)
        else:
            shave_es(dart_context, json.loads(query), count)
    else:
        with open(query_file, 'rt') as qf:
            query_from_file = qf.read()
            if corpex:
                shave(dart_context, json.loads(query_from_file), count)
            else:
                shave_es(dart_context, json.loads(query_from_file), count)

def map_doc_id(hit_obj):
    return hit_obj['_source']['document_id']

def shave_es(dart_context, query_text, take):
    query_obj = json.loads(query_text)
    if '_source' in query_obj:
        query_obj.pop('_source')
    if 'stored_fields' in query_obj:
        query_obj.pop('stored_fields')
    if 'from' in query_obj:
        query_obj.pop('from')
    query_obj['size'] = 2000
    query = json.dumps(query_obj)

    response = start_scroll(dart_context, query)
    if response.status_code > 200:
        raise Exception(f'Could not search elasticsearch: {response.text}')

    response_json = response.text
    response_obj = json.loads(response_json)
    scroll_id = response_obj['_scroll_id']
    results = response_obj['hits']['hits']
    count = len(results)
    docs = list(map(map_doc_id, results))
    for doc_id in docs[0:take]:
        print(doc_id)

    total_count = count

    while count >= 0 and total_count < take:
        response = continue_scroll(dart_context, scroll_id)
        if response.status_code > 200:
            raise Exception(f'Could not search elasticsearch: {response.text}')

        response_json = response.text
        response_obj = json.loads(response_json)
        results = response_obj['hits']['hits']
        count = len(results)
        if count == 0:
            break

        docs = list(map(map_doc_id, results))
        for doc_id in docs[0:take - total_count]:
            print(doc_id)

        total_count += count
