import click
from click import Context

from dart_context.dart_config import DartConfigException
from dart_context.dart_context import DartContext

from cli.global_options import dart_options, pass_dart_context
from pipeline.clean import clean_s3, get_opts, stop_containers_clear_data
from pipeline.deploy import deploy
from pipeline.diab import deploy_diab, stop_diab, start_diab, clean_diab, destroy_diab
from pipeline.provision import provision, destroy, start_pipeline, stop_pipeline, info_pipeline


@click.command(name='provision')
@dart_options
@pass_dart_context
def provision_command(dart_context: DartContext):
    """Provisioning DART infrastructure"""
    if not dart_context.dart_env.is_tst():
        raise DartConfigException(f'unable to provision for {dart_context.dart_env.env_type()} environment. Only TST deployment environments can be provisioned.')

    provision(dart_context)


@click.command(name='deploy')
@dart_options
@click.option('--ec2-ini-path', default=None, help='Path to an ec2.ini configuration (TST deployment environment only)')
@pass_dart_context
def deploy_command(dart_context: DartContext, ec2_ini_path):
    """Deploy DART services"""
    if dart_context.dart_env.is_default():
        choice = None
        while choice is None:
            y_or_n = input('This will deploy Dart-in-a-Box, erasing any saved data. Are you sure you want to proceed? (Y/n) ')
            if y_or_n == 'Y':
                choice = True
            if y_or_n == 'n':
                choice = False
        if choice:
            deploy_diab(dart_context)
        else:
            return
    elif dart_context.dart_env.is_tst():
        deploy(dart_context, ec2_ini_path)
    else:
        raise click.ClickException('Deploy command unsupported for custom deployment environment')


@click.command(name='refresh')
@dart_options
@click.option('--ec2-ini-path', default=None, help='Path to an ec2.ini configuration')
@click.option('--save-raws', is_flag=True, default=False, help='Preserves raws documents in s3')
@pass_dart_context
def refresh_command(dart_context: DartContext, ec2_ini_path, save_raws):
    """Clear data and redeploy all DART services"""
    if dart_context.dart_env.is_default():
        return deploy_diab(dart_context)
    if not dart_context.dart_env.is_tst():
        raise DartConfigException(f'refresh not supported for {dart_context.dart_env.env_type()} deployment. Only default and TST deployment environments can be refreshed.')

    print(f'Warning! Running this command will delete all data in {dart_context.dart_env.tst_env.env}')
    res = input('Do you wish to proceed (n/Y)   ')
    if res != 'Y':
        print('aborting...')
        exit(1)
    status = True
    if not save_raws:
        status = clean_s3(dart_context, get_opts(dart_context, True))
    if status:
        if stop_containers_clear_data(dart_context, ec2_ini_path):
            if not deploy(dart_context, ec2_ini_path):
                print('Redeployment of services failed')
        else:
            print('Failed to stop services and/or clear data')
    else:
        print('Failed to clean s3 buckets (aborted)')


@click.command(name='provision-deploy')
@dart_options
@click.option('--ec2-ini-path', default=None, help='Path to an ec2.ini configuration')
@pass_dart_context
def provision_deploy_command(dart_context: DartContext, ec2_ini_path):
    """DART cli command for provisioning and deploying DART infrastructure"""
    if not dart_context.dart_env.is_tst():
        raise DartConfigException(f'unable to provision for {dart_context.dart_env.env_type()} environment. Only TST deployment environments can be provisioned.')

    provision_success = provision(dart_context)
    if provision_success:
        deploy(dart_context, ec2_ini_path)
    else:
        print('Provision failed -- cancelling deployment')


@click.command(name='destroy')
@dart_options
@pass_dart_context
def destroy_command(dart_context: DartContext):
    """DART cli command for tearing down DART infrastructure"""
    if dart_context.dart_env.is_default():
        return destroy_diab(dart_context)
    if not dart_context.dart_env.is_tst():
        raise DartConfigException(f'destroy not supported for {dart_context.dart_env.env_type()} deployment. Only default and TST deployment environments can be destroyed.')

    print(f'Warning! Running this command will remove all service infrastructure in {dart_context.dart_env.tst_env.env}')
    res = input('Do you wish to proceed (n/Y)   ')
    if res != 'Y':
        print('aborting...')
        exit(1)
    destroy(dart_context)


@click.command(name='start')
@dart_options
@pass_dart_context
def start_command(dart_context : DartContext):
    """Start all stopped DART instances"""
    if dart_context.dart_env.env_type() == 'default':
        return start_diab(dart_context)

    if dart_context.aws_profile is None:
        raise click.exceptions.MissingParameter( "missing aws profile: --aws-profile" )
    if dart_context.dart_env.tst_env.env is None:
        raise click.exceptions.MissingParameter( "missing DART environment: --env/-e" )
    start_pipeline(dart_context)


@click.command(name='stop')
@dart_options
@pass_dart_context
def stop_command(dart_context: DartContext):
    """Stop all DART instances"""
    if dart_context.dart_env.env_type() == 'default':
        return stop_diab(dart_context)

    if not dart_context.dart_env.is_tst():
        raise DartConfigException(f'destroy not supported for {dart_context.dart_env.env_type()} deployment. Only default and TST deployments can be stopped.')

    if dart_context.aws_profile is None:
        raise click.exceptions.MissingParameter( "missing aws profile: --aws-profile" )
    if dart_context.dart_env.tst_env.env is None:
        raise click.exceptions.MissingParameter( "missing DART environment: --env/-e" )
    stop_pipeline(dart_context)


@click.command(name='info')
@dart_options
@pass_dart_context
def info_command(dart_context: DartContext):
    """Stop all DART instances"""
    if not dart_context.dart_env.is_tst:
        raise DartConfigException(f'info command is unsupported for {dart_context.dart_env.env_type()} deployment environment. Only TST deployments can provide info')

    if dart_context.aws_profile is None:
        raise click.exceptions.MissingParameter( "missing aws profile: --aws-profile" )
    if dart_context.dart_env.tst_env.env is None:
        raise click.exceptions.MissingParameter( "missing DART environment: --env/-e" )
    info_pipeline(dart_context)


@click.command(name='clean-s3')
@dart_options
@click.option('--no-prompt/--prompt', default=False)
@pass_dart_context
def clean_command(dart_context, no_prompt):
    """Empty all contents of an environment's s3 buckets"""
    if dart_context.dart_env.is_default():
        return clean_diab(dart_context)
    if not dart_context.dart_env.is_tst():
        raise DartConfigException(f'clean not supported for {dart_context.dart_env.env_type()} deployment. Only default and TST deployment environments can be cleaned.')

    if not no_prompt:
        print(f'Warning! Running this command will delete all stored raw documents and upload metadata in {dart_context.dart_env.tst_env.env}')
        res = input('Do you wish to proceed (n/Y)   ')
        if res != 'Y':
            print('aborting...')
            exit(1)

    clean_s3(dart_context, get_opts(dart_context, no_prompt))


@click.command(name='nuke')
@dart_options
@pass_dart_context
@click.pass_context
def nuke_command(ctx: Context, dart_context: DartContext):
    """Destroy an existing DART environment"""
    ctx.invoke(destroy_command)
    ctx.invoke(clean_command, no_prompt=False)
