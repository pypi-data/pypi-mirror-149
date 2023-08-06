import base64
from abc import ABC, abstractmethod
from typing import Callable

from dart_context.dart_config import DartConfig, DartConfigException
from utilities.auth import update_token


class AuthConfigType(DartConfig, ABC):
    """
    Abstract configuration type that can generate authorization headers for
    DART REST clients
    """

    @abstractmethod
    def auth_headers(self, dart_context: 'DartContext') -> dict[str, str]:
        """
        Generate headers necessary for making a REST call
        """
        pass

    @abstractmethod
    def refresh_auth(self, dart_context: 'DartContext') -> None:
        """
        Refresh auth token if there is one
        """
        pass


class NoAuthConfigType(AuthConfigType):
    def auth_headers(self, dart_context: 'DartContext') -> dict[str, str]:
        return {}

    def refresh_auth(self, dart_context: 'DartContext') -> None:
        return

    def sub_config_fields(self) -> dict[str, 'DartConfig']:
        return {}

    def primitive_fields(self) -> dict[str, (Callable[[], any], Callable[[any], None])]:
        return {}


class BasicAuthConfigType(AuthConfigType):
    basic_username: str = None
    basic_password: str = None

    def auth_headers(self, dart_context: 'DartContext') -> dict[str, str]:
        cred_str = f'{self.basic_username}:{self.basic_password}'
        cred_str_encoded = base64.b64encode(cred_str.encode('utf-8')).decode('utf-8')
        return {'Authorization': f'Basic {cred_str_encoded}'}

    # No need to refresh with static credentials
    def refresh_auth(self, dart_context: 'DartContext') -> None:
        return

    def set_auth(self, creds):
        split_auth = creds.split(':')
        [self.basic_username, self.basic_password] = split_auth

    def set_username(self, un):
        self.basic_username = un

    def set_password(self, pw):
        self.basic_password = pw

    def sub_config_fields(self) -> dict[str, DartConfig]:
        return {}

    def primitive_fields(self) -> dict[str, (Callable[[], any], Callable[[any], None])]:
        return {
            'username': (lambda: self.basic_username, lambda un: self.set_username(un)),
            'password': (lambda: self.basic_password, lambda pw: self.set_password(pw)),
        }


DEFAULT_USE_CLIENT_SECRET = True


class DartAuthConfigType(AuthConfigType):
    dart_username: str = None
    dart_password: str = None
    client_secret: str = None
    token: str = None
    __use_client_secret_flag: bool = None

    def use_client_secret(self) -> bool:
        if self.__use_client_secret_flag is None:
            return DEFAULT_USE_CLIENT_SECRET
        else:
            return self.__use_client_secret_flag

    def set_auth(self, creds):
        split_auth = creds.split(':')
        if len(split_auth) == 2:
            [self.dart_username, self.dart_password] = split_auth
        else:
            self.client_secret = creds

    def set_dart_username(self, un):
        self.dart_username = un

    def set_dart_password(self, pw):
        self.dart_password = pw

    def set_client_secret(self, secret):
        self.client_secret = secret

    def use_client(self):
        self.__use_client_secret_flag = True

    def use_login(self):
        self.__use_client_secret_flag = False

    def update_token(self, new_token):
        self.token = new_token

    def sub_config_fields(self) -> dict[str, DartConfig]:
        return {}

    def primitive_fields(self) -> dict[str, (Callable[[], any], Callable[[any], None])]:
        return {
            'username': (lambda: self.dart_username, lambda un: self.set_dart_username(un)),
            'password': (lambda: self.dart_password, lambda pw: self.set_dart_password(pw)),
            'client_secret': (lambda: self.client_secret, lambda cs: self.set_client_secret(cs)),
            'token': (lambda: self.token, lambda tk: self.update_token(tk)),
            'use_client_secret': (lambda: self.__use_client_secret_flag,
                                  lambda ucs: self.use_client() if ucs else self.use_login()),
        }

    def auth_headers(self, dart_context: 'DartContext') -> dict[str, str]:
        if self.token is None:
            self.refresh_auth(dart_context)
        return {'Authorization': f'Bearer {self.token}'}

    def refresh_auth(self, dart_context: 'DartContext') -> None:
        new_token = update_token(dart_context, False, False)
        if new_token is not None:
            self.token = new_token


DEFAULT_AUTH_TYPE = 'no_auth'


class AuthConfig(AuthConfigType):
    dart_auth_config: DartAuthConfigType = DartAuthConfigType()
    basic_auth_config: BasicAuthConfigType = BasicAuthConfigType()
    no_auth_config: NoAuthConfigType = NoAuthConfigType()

    __auth_type: str = None

    def auth_type(self) -> str:
        if self.__auth_type is None:
            return DEFAULT_AUTH_TYPE
        return self.__auth_type

    def set_auth_type(self, new_type: str) -> None:
        self.__auth_type = new_type

    def set_auth_type_none(self) -> None:
        self.set_auth_type('no_auth')

    def set_auth_type_basic(self) -> None:
        self.set_auth_type('basic')

    def set_auth_type_dart(self) -> None:
        self.set_auth_type('dart')

    def __selected_auth_config(self) -> AuthConfigType:
        if self.auth_type() == 'no_auth':
            return self.no_auth_config
        elif self.auth_type() == 'dart':
            return self.dart_auth_config
        elif self.auth_type() == 'basic':
            return self.basic_auth_config
        else:
            raise DartConfigException(f'invalid auth type: {self.auth_type()}')

    def auth_headers(self, dart_context: 'DartContext') -> dict[str, str]:
        return self.__selected_auth_config().auth_headers(dart_context)

    def refresh_auth(self, dart_context: 'DartContext') -> None:
        return self.__selected_auth_config().refresh_auth(dart_context)

    def sub_config_fields(self) -> dict[str, 'DartConfig']:
        return {
            'dart_auth': self.dart_auth_config,
            'basic_auth': self.basic_auth_config,
            'no_auth': self.no_auth_config,
        }

    def primitive_fields(self) -> dict[str, (Callable[[], any], Callable[[any], None])]:
        return {
            'auth_type': (lambda: self.__auth_type, lambda at: self.set_auth_type(at)),
        }