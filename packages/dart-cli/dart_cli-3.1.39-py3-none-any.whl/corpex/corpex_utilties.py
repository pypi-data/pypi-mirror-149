import uuid

import requests
import json

from dart_context.dart_context import DartContext

from utilities import url
from utilities.auth import generate_auth_headers


def start_scroll(dart_context: DartContext, query):
    scroll_url = 'http://' + url.get_host('search', dart_context) + ':9200/cdr_search/_search?scroll=1m'
    return requests.post(scroll_url, json=json.loads(query))

def continue_scroll(dart_context: DartContext, scroll_id):
    json_data = {
        'scroll': '1m',
        'scroll_id': scroll_id,
    }
    scroll_url = 'http://' + url.get_host('search', dart_context) + ':9200/_search/scroll'
    return requests.post(scroll_url, json=json_data)

def search(dart_context: DartContext, query):
    search_url = url.get_base_url('corpex', dart_context) + '/search'
    auth_headers = generate_auth_headers(dart_context)
    with requests.post(search_url, json=query, headers=auth_headers) as response:
        if response.status_code != 200:
            raise Exception(f'Search status: {response.status_code}:\n{response.text}')
        return response.json()

def count(dart_context: DartContext, query):
    search_url = url.get_base_url('corpex', dart_context) + '/search/count'
    auth_headers = generate_auth_headers(dart_context)
    with requests.post(search_url, json=query, headers=auth_headers) as response:
        if response.status_code != 200:
            raise Exception(f'Count status: {response.status_code}:\n{response.text}')
        return response.json()['num_results']

def shave(dart_context: DartContext, query, take):
    search_url = url.get_base_url('corpex', dart_context) + '/search/shave?take=' + str(take)
    auth_headers = generate_auth_headers(dart_context)

    if len(dart_context.tenants()) > 0:
        query['tenant_id'] = dart_context.tenants()[0]

    with requests.post(search_url, json=query, headers=auth_headers) as response:
        if response.status_code != 200:
            raise Exception(f'Count status: {response.status_code}:\n{response.text}')
        for doc_id in response.json():
            print(doc_id)

def aggregate_corpus(dart_context: DartContext, corpex_query, aggs):
    """Submit and return aggregation over corpex-filtered collection"""
    search_url = url.get_base_url('corpex', dart_context) + '/search'
    print(search_url)
    query = {
        'page_size': 0,
        'fields': [],
        'queries': corpex_query['queries'],
        'aggregations': aggs
    }

    auth_headers = generate_auth_headers(dart_context)
    with requests.post(search_url, json=query, headers=auth_headers) as response:
        if response.status_code != 200:
            raise Exception(f'Search status: {response.status_code}:\n{response.text}')
        return response.json()

