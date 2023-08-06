import os
import json
import click
from dart_context.dart_context import DartContext

from cli.global_options import dart_options, pass_dart_context

def dart_dir():
    home = os.getenv('HOME')
    return os.path.join(home, '.dart')

@click.command(name='add')
@dart_options
@click.argument('profile_name', required=True)
@pass_dart_context
def add_profile_command(dart_context: DartContext, profile_name):
    """Add a DART profiles"""
    dart_context.save_profile(profile_name)

@click.command(name='rm')
@click.argument('profiles', required=True, nargs=-1)
@dart_options
def remove_profile_command(profiles):
    """Remove one or more DART profiles"""
    for profile_name in profiles:
        profile_path = os.path.join(dart_dir(), profile_name + '.conf')
        try:
            os.remove(profile_path)
        except FileNotFoundError:
            print(f'profiles {profile_name} does not exist')

@click.command(name='ls')
@dart_options
def ls_profiles_command():
    """List all DART profiles"""
    for (_, _, filenames) in os.walk(dart_dir()):
        for filename in filenames:
            split_name = filename.split('.')
            if len(split_name) == 2:
                [profile, ext] = split_name
                if ext == 'conf':
                    print(profile)

@click.command(name='view')
@click.argument('profile_name', required=False)
@dart_options
@pass_dart_context
def view_profile_command(ctx : DartContext, profile_name):
    """View a DART profile, or current configuration of none specified"""
    if profile_name is not None:
        profile_path = os.path.join(dart_dir(), profile_name + '.conf')
        with open(profile_path, 'rt') as profile_file:
            print(profile_file.read())
    else:
        print(json.dumps(ctx.to_dict(), indent=4))
