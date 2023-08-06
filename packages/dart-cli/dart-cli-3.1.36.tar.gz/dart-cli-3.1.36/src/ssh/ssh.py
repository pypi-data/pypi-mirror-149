import os

from utilities.url import get_host

from dart_context.dart_context import DartContext


def open_ssh(dart_context: DartContext, node: str):
    key_path = os.path.join(os.getenv("HOME"), '.ssh', dart_context.ssh_key)
    key_opt = '' if key_path is None else f' -i {key_path}'
    host = get_host(node, dart_context)
    host_param = f'ubuntu@{host}'
    command = f'ssh{key_opt} {host_param}'
    print(command)
    os.system(command)
