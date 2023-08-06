import jwt
import requests

from utilities.url import get_base_url


def generate_auth_headers(dart_context: 'DartContext') -> dict[str, str]:
    return dart_context.auth_config.auth_headers(dart_context)



KEYCLOAK_REALM = 'dart'
KEYCLOAK_PROTOCOL = 'openid-connect'
KEYCLOAK_CLIENT = 'dart-cli'

def update_token(context: 'DartContext', show: bool, decode: bool) -> str:
    base_url = get_base_url('keycloak', context)
    if context.auth_config.dart_auth_config.use_client_secret() and context.auth_config.dart_auth_config.client_secret is not None:
        keycloak_url = f'{base_url}/auth/realms/{KEYCLOAK_REALM}/protocol/{KEYCLOAK_PROTOCOL}/token'
        client_secret = context.auth_config.dart_auth_config.client_secret
        res = requests.post(keycloak_url, data={'grant_type': 'client_credentials',
                                                'client_id': KEYCLOAK_CLIENT,
                                                'client_secret': client_secret})
        if res.status_code == 200:
            res_data = res.json()
            new_token = res_data['access_token']
            if show:
                print(new_token)
            if decode:
                print(jwt.decode(new_token, options={"verify_signature": False}))
            return new_token
        else:
            print("Unable to update token:")
            print(res.json())
