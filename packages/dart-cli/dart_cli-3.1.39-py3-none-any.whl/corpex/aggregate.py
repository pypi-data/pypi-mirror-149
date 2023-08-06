import json
from collections import OrderedDict
from io import StringIO
import csv

import click

from corpex.corpex_utilties import aggregate_corpus
from dart_context.dart_context import DartContext
from cli.global_options import pass_dart_context, dart_options

def execute_corpus_stats(dart_context: DartContext, corpex_query: dict, output_format: str, output_path: str):
    """Execute corpus stats query and display results"""
    raise NotImplementedError()

def execute_corpus_agg(dart_context: DartContext, corpex_query: dict, agg_query: dict, output_format: str, output_path: str):
    """Execute and display results of a corpus agg query"""
    aggs = {
        'aggregation_id': agg_query
    }
    if len(corpex_query['queries']) > 0:
        print(f'Corpex queries: {corpex_query["queries"]}')
    print(f'Aggregation query: {agg_query}')
    response = aggregate_corpus(dart_context, corpex_query, aggs)
    formatted_results = generate_corpus_agg_results(response, output_format)
    output_results(formatted_results, output_path)

def generate_corpus_agg_results(results: dict, output_format: str):
    """Output list of doc counts"""
    if output_format == 'json':
        return results['aggregations']['aggregation_id']
    if output_format == 'csv' or output_format == 'tsv':
        delimiter = ',' if output_format == 'csv' else '\t'
        csv_file = StringIO()
        all_results: dict = results['aggregations']['aggregation_id']
        fieldnames = OrderedDict()
        for key in all_results[0].keys():
            fieldnames[key] = None
        dict_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=delimiter)
        dict_writer.writeheader()
        dict_writer.writerows(all_results)
        csv_file.seek(0)
        writer_output = csv_file.read()
        csv_file.close()
        return writer_output

def output_results(results: str, output_path: str):
    if output_path is None:
        print(results)
    else:
        with open(output_path, 'wt') as output_file:
            output_file.write(results)

def parse_number(number_string):
    """Return int if int, float if float, or string if neither"""
    try:
        number_float = float(number_string)
        if number_float.is_integer():
            return int(number_float)
        else:
            return number_float
    except ValueError:
        return number_string

@click.command(name='corpus')
@dart_options
@click.option('-a', '--agg-query', required=False, help='Aggregation query json')
@click.option('-A', '--agg-file', required=False, help='Aggregation query json file')
@click.option('--corpus-stats/--custom-query', default=False,
              help='Get standard aggregations (overrides all other options except --corpex-query/--corpex-file')
@click.option('-c', '--corpex-query', required=False, help='Corpex query json')
@click.option('-C', '--corpex-file', required=False, help='Corpex query json file')
@click.option('-t', '--agg-type', type=click.Choice(['FIELD', 'TAG_TYPES', 'TAG_VALUES', 'FACET'], case_sensitive=True))
@click.option('-s', '--size', help='Number of aggregations to return')
@click.option('-q', '--query-string', help='Query to filter values')
@click.option('-f', '--field', help='Corpex field to aggregate (FIELD type aggs only)')
@click.option('-b', '--bucket-size', help='Set bucket size for FIELD agg query on numerical or date fields')
@click.option('-l', '--low-bound',
              help='Lower bound for numerical FIELD aggregations or lower bound of confidence for FACET aggregations')
@click.option('-h', '--high-bound',
              help='Upper bound for numerical FIELD aggregations or upper bound of confidence for FACET aggregations')
@click.option('--tag-id', help='Tag id for TAG_TYPES and TAG_VALUES aggregations')
@click.option('--tag-type', multiple=True,
              help='Tag types for TAG_VALUES aggregations (can be used multiple times to include multiple values')
@click.option('--exact-tag-types/--fuzzy-tag-types', default=False,
              help='Determine whether tag types will filter exact match or fuzzy match')
@click.option('--tag-types-query', help='Query for tag type (only for TAG_VALUES aggregations)')
@click.option('--facet-id', help='Facet id for FACET aggregations')
@click.option('-F', '--format', 'output_format', type=click.Choice(['json', 'csv', 'tsv'], case_sensitive=False), help='Output format (json|csv|tsv')
@click.option('-o', '--output', help='Save output as a file')
@pass_dart_context
def aggregate_corpus_command(dart_context: DartContext, agg_query, agg_file, corpus_stats, corpex_query, corpex_file,
                             agg_type, size, query_string, field, bucket_size, low_bound, high_bound, tag_id, tag_type,
                             exact_tag_types, tag_types_query, facet_id, output_format, output):
    """Get aggregations over the collection or a subset defined by a corpex search"""
    # Validate parameters a little bit
    if agg_query is not None and agg_file is not None:
        raise click.exceptions.BadOptionUsage('--agg-query/--agg-file', 'Cannot use --agg-query and --agg-file')
    if corpex_query is not None and corpex_file is not None:
        raise click.exceptions.BadOptionUsage('--corpex-query/--corpex-file',
                                              'Cannot use --corpex-query and --corpex-file')

    corpex_query_dict = {'queries': []}
    if corpex_query is not None:
        corpex_query_dict = json.loads(corpex_query)
    if corpex_file is not None:
        with open(corpex_file, 'rt') as open_corpex_file:
            corpex_query_dict = json.loads(open_corpex_file.read())
    corpex_query_dict['page_size'] = 0
    corpex_query_dict['fields'] = []

    if corpus_stats:
        execute_corpus_stats(dart_context, corpex_query_dict, output_format, output)
        return

    if agg_query is not None:
        agg_query_dict = json.loads(agg_query)
        execute_corpus_agg(dart_context, corpex_query_dict, agg_query_dict, output_format, output)
        return

    agg_query_dict = {}
    if agg_type is None:
        raise click.MissingParameter('If no agg query is provided (--agg-query/--agg-file), --agg-type is required')
    agg_query_dict['agg_type'] = agg_type
    if size is not None:
        agg_query_dict['size'] = size
    if agg_type == 'FIELD':
        if field is None:
            raise click.MissingParameter('--field is required for FIELD aggregation')
        agg_query_dict['queried_field'] = field
        if query_string is not None:
            agg_query_dict['values_query'] = query_string
        if bucket_size is not None:
            agg_query_dict['bucket_size'] = parse_number(bucket_size)
        if low_bound is not None:
            agg_query['lo'] = parse_number(low_bound)
        if high_bound is not None:
            agg_query['hi'] = parse_number(high_bound)
    if agg_type == 'TAG_TYPES':
        if tag_id is None:
            raise click.MissingParameter('--tag-id is required for TAG_TYPES aggregation')
        agg_query_dict['tag_id'] = tag_id
        if query_string is not None:
            agg_query_dict['tag_types_query'] = query_string
    if agg_type == 'TAG_VALUES':
        if tag_id is None:
            raise click.MissingParameter('--tag-id is required for TAG_TYPES aggregation')
        agg_query_dict['tag_id'] = tag_id
        if tag_types_query is not None:
            agg_query_dict['tag_types_query'] = tag_types_query
        if tag_type is not None:
            if exact_tag_types:
                agg_query_dict['tag_types_exact'] = tag_type
            else:
                agg_query_dict['tag_types'] = tag_type
        if query_string is not None:
            agg_query_dict['tag_values_query'] = query_string
    if agg_type == 'FACET':
        if facet_id is None:
            raise click.MissingParameter('--facet-id is required for FACET aggregation')
        agg_query_dict['facet_id'] = facet_id
        if query_string is not None:
            agg_query_dict['facet_values_query'] = query_string
        if low_bound is not None:
            agg_query_dict['conf_lo'] = float(low_bound)
        if high_bound is not None:
            agg_query_dict['conf_hi'] = float(high_bound)

    print(agg_query_dict)
    execute_corpus_agg(dart_context, corpex_query_dict, agg_query_dict, output_format, output)


@click.group(name='aggregate')
@dart_options
@pass_dart_context
def aggregate_command(dart_context: DartContext):
    """Commands for aggregating CDR data"""

aggregate_command.add_command(aggregate_corpus_command)
