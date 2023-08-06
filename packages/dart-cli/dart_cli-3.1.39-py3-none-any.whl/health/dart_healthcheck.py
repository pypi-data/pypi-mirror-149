import requests

from utilities.auth import generate_auth_headers
from utilities.url import get_base_url

from dart_context.dart_context import DartContext

def check_health(context: DartContext, service):
    base_url = get_base_url(service, context)
    msg_prefix = (service + ':                           ')[:20]
    url = base_url + '/health'
    auth_headers = generate_auth_headers(context)

    try:
        response = requests.get(url, headers=auth_headers)
    except Exception as e:
        return False, f'{msg_prefix}Failed - Unable to reach service: {str(e)}'

    try:
        response.raise_for_status()
    except Exception as e:
        return False, f'{msg_prefix}Failed - Unable to reach health service: {str(response.status_code)} - {response.text[0:200]}'

    try:
        response_data = response.json()
        status = response_data['status']
        version = ''
        msg = ''
        if 'version' in response_data:
            version = f'v{response_data["version"]} '
        if 'message' in response_data:
            msg = ' - ' + response_data['message']
        return status != 'UNHEALTHY', f'{msg_prefix}{version}{status}{msg}'
    except Exception as e:
        return False, f'{msg_prefix}Failed (unable to read health-check response: {response.text})'