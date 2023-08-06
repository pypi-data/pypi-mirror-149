import click

from cli.global_options import dart_options, pass_dart_context
from dart_context.dart_context import DartContext
from utilities.auth import update_token


@click.command(name='retrieve-token')
@dart_options
@click.option('--decode-only', is_flag=True, flag_value=True, default=False)
@click.option('--decode', is_flag=True, flag_value=True, default=False)
@pass_dart_context
def command(context : DartContext, decode_only, decode):
    """Update token used to authenticate/authorize DART services"""
    new_token = update_token(context, not decode_only, decode or decode_only)
    context.auth_config.dart_auth_config.update_token(new_token)
