import click
from utilities.aws import query_metadata

from dart_context.dart_context import DartContext

pass_dart_context = click.make_pass_decorator(DartContext, ensure=True)


def profile_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(DartContext)
        if value is not None:
            state.from_profile(value)
        return value
    return click.option('-p', '--profile',
                        is_eager=True,
                        expose_value=False,
                        help='Use DART configuration profile (~/.dart/[profile].conf)',
                        callback=callback)(f)


def env_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.dart_env.tst_env.set_env(value)
        return value
    return click.option('-e', '--env',
                        is_eager=False,
                        expose_value=False,
                        help='Use TST-DART deployment environment.',
                        callback=callback)(f)


def env_choice_cb(ctx, param, value):
    state: DartContext = ctx.ensure_object(DartContext)
    if value is not None:
        state.dart_env.set_env_type(value)
    return value


def use_default_env_option(f):
    return click.option('--default-env',
                        'env_choice',
                        expose_value=False,
                        flag_value="default",
                        help='Configure for default deployment environment (cannot use with --tst-env or --custom-env)',
                        callback=env_choice_cb)(f)


def use_tst_env_option(f):
    return click.option('--tst-env',
                        'env_choice',
                        expose_value=False,
                        flag_value="tst",
                        help='Configure for TST deployment environment (cannot use with --default-env or --custom-env)',
                        callback=env_choice_cb)(f)


def use_custom_env_option(f):
    return click.option('--custom-env',
                        'env_choice',
                        expose_value=False,
                        flag_value="custom",
                        help='Configure for custom deployment environment (cannot use with --default-env or --custom-env).',
                        callback=env_choice_cb)(f)


def remote_deployment_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.dart_env.default_env.set_host(value)
        return value
    return click.option('--remote',
                        is_eager=False,
                        expose_value=False,
                        help='Set remote host of dart-in-a-box deployment.',
                        callback=callback)(f)


def tst_user_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.dart_env.tst_env.set_ssh_user(value)
        return value
    return click.option('--tst-user',
                        is_eager=False,
                        expose_value=False,
                        help='Set user for remote (ssh) deployment of TST deployment environment.',
                        callback=callback)(f)


def diab_user_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.dart_env.default_env.set_user(value)
        return value
    return click.option('--diab-user',
                        is_eager=False,
                        expose_value=False,
                        help='Set user for remote (ssh) deployment of Dart-in-a-Box.',
                        callback=callback)(f)


def diab_dir_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.dart_env.default_env.set_data_dir(value)
        return value
    return click.option('--diab-dir',
                        is_eager=False,
                        expose_value=False,
                        help='Set working directory for local or remote deployment of Dart-in-a-Box.',
                        callback=callback)(f)


def diab_version_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.dart_env.default_env.set_version(value)
        return value
    return click.option('--diab-version',
                        is_eager=False,
                        expose_value=False,
                        help='Set Dart-in-a-Box version for deployment.',
                        callback=callback)(f)


def local_deployment_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value:
            state.dart_env.default_env.set_host(None)
        return value
    return click.option('--local',
                        is_eager=False,
                        flag_value=True,
                        default=False,
                        expose_value=False,
                        help='Configure for local deployment of dart-in-a-box (default).',
                        callback=callback)(f)


def aws_env_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.dart_env.tst_env.set_aws_environment(value)
        return value
    return click.option('--aws-environment',
                        is_eager=False,
                        expose_value=False,
                        type=click.Choice(['dart', 'prod'], case_sensitive=False),
                        help='Choose AWS account to use for pipeline deployment.',
                        callback=callback)(f)


def basic_auth_creds(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.auth_config.basic_auth_config.set_auth(value)
        return value
    return click.option('--basic-login',
                        is_eager=False,
                        expose_value=False,
                        help='Set basic auth credentials for DART services (username:password).',
                        callback=callback)(f)


def basic_username_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.auth_config.basic_auth_config.set_username(value)
        return value
    return click.option('--basic-username',
                        is_eager=False,
                        expose_value=False,
                        help='Set username for basic auth.',
                        callback=callback)(f)


def basic_password_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.auth_config.basic_auth_config.set_password(value)
        return value
    return click.option('--basic-password',
                        is_eager=False,
                        expose_value=False,
                        help='Set password for basic auth.',
                        callback=callback)(f)


def dart_secret_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.auth_config.dart_auth_config.set_client_secret(value)
        return value
    return click.option('--dart-secret',
                        is_eager=False,
                        expose_value=False,
                        help='Set dart-cli client secret for DART authentication and authorization.',
                        callback=callback)(f)


def dart_login_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            parsed = value.split(':')
            if len(parsed) != 2:
                raise click.exceptions.BadOptionUsage('dart-login', 'Separate username and password with a single colon.')
            state.auth_config.dart_auth_config.set_auth(value)
        return value
    return click.option('--dart-login',
                        is_eager=False,
                        expose_value=False,
                        help='Set username and password for dart auth. Usage: --dart-login [username]:[password].',
                        callback=callback)(f)


def dart_username_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.auth_config.dart_auth_config.set_dart_username(value)
        return value
    return click.option('--dart-username',
                        is_eager=False,
                        expose_value=False,
                        help='Set username for dart auth.',
                        callback=callback)(f)


def dart_password_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.auth_config.dart_auth_config.set_dart_password(value)
        return value
    return click.option('--dart-password',
                        is_eager=False,
                        expose_value=False,
                        help='Set password for dart auth.',
                        callback=callback)(f)


def auth_option_cb(ctx, param, value):
    state: DartContext = ctx.ensure_object(DartContext)
    if value is not None:
        state.auth_config.set_auth_type(value)
    return value

def no_auth_option(f):
    return click.option('--no-auth',
                        'auth_choice',
                        expose_value=False,
                        flag_value="no_auth",
                        help='Don\'t use auth (cannot use with --dart-auth or --basic-auth)',
                        callback=auth_option_cb)(f)


def basic_auth_option(f):
    return click.option('--basic-auth',
                        'auth_choice',
                        expose_value=False,
                        flag_value='basic',
                        help='Use basic auth (cannot use with --dart-auth or --no-auth)',
                        callback=auth_option_cb)(f)


def dart_auth_option(f):
    return click.option('--dart-auth',
                        'auth_choice',
                        expose_value=False,
                        flag_value='dart',
                        help='Use dart auth (cannot use with --basic-auth or --no-auth)',
                        callback=auth_option_cb)(f)


def use_dart_public_login_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            if value:
                state.auth_config.dart_auth_config.use_login()
        return value

    return click.option('--dart-public/--dart-client',
                        expose_value=False,
                        default=None,
                        help='Use public login flow or dart client auth flow to access DART services',
                        callback=callback)(f)


def dart_tenant_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None and len(value) > 0:
            state.add_tenants(list(value))
        return value

    return click.option('--tenant',
                        is_eager=False,
                        expose_value=False,
                        help='Provide a tenant. Can be used multiple times.',
                        multiple=True,
                        default=[],
                        callback=callback)(f)


def aws_profile_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.set_aws_profile(value)
        return value
    return click.option('--aws-profile',
                        is_eager=False,
                        expose_value=False,
                        help='Profile to be used for AWS services',
                        callback=callback)(f)


def ssh_public_key_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.set_ssh_key(value)
        return value
    return click.option('--ssh-key',
                        is_eager=False,
                        expose_value=False,
                        help='SSH public key (path) for deploying DART services',
                        callback=callback)(f)


def dart_version_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            try:
                [project_id, version] = value.split(':')
                state.dart_env.tst_env.set_project_id(project_id.strip())
                state.dart_env.tst_env.set_pipeline_version(version.strip())
            except:
                raise click.exceptions.BadOptionUsage('dart-version', 'dart-version must include the project id (wm, dev) and the pipeline version separated by a colon')
        return value
    return click.option('--dart-version',
                        is_eager=False,
                        expose_value=False,
                        help='DART project id and pipeline version separated by colon, e.g., wm:3.0.1',
                        callback=callback)(f)


def kafka_auth_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            [un, pw] = value.split(':')
            state.kafka_config.sasl_config.set_username(un.strip())
            state.kafka_config.sasl_config.set_password(pw.strip())
        return value

    return click.option('--kafka-login',
                        is_eager=False,
                        expose_value=False,
                        help='Provide kafka SASL credentials (username:password).',
                        callback=callback)(f)


def kafka_username_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.kafka_config.sasl_config.set_username(value)
        return value

    return click.option('--kafka-username',
                        is_eager=False,
                        expose_value=False,
                        help='Provide kafka username.',
                        callback=callback)(f)


def kafka_password_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.kafka_config.sasl_config.set_password(value)
        return value

    return click.option('--kafka-password',
                        is_eager=False,
                        expose_value=False,
                        help='Provide kafka password.',
                        callback=callback)(f)


def docker_auth_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            [un, pw] = value.split(':')
            state.docker_config.set_docker_username(un.strip())
            state.docker_config.set_docker_password(pw.strip())
        return value

    return click.option('--docker-login',
                        is_eager=False,
                        expose_value=False,
                        help='Provide docker credentials (username:password).',
                        callback=callback)(f)


def docker_username_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.docker_config.set_docker_username(value)
        return value

    return click.option('--docker-username',
                        is_eager=False,
                        expose_value=False,
                        help='Provide docker username.',
                        callback=callback)(f)

def docker_password_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.docker_config.set_docker_password(value)
        return value

    return click.option('--docker-password',
                        is_eager=False,
                        expose_value=False,
                        help='Provide docker password.',
                        callback=callback)(f)


def docker_registry_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.docker_config.set_docker_registry_host(value)
        return value

    return click.option('--docker-registry',
                        is_eager=False,
                        expose_value=False,
                        help='Docker registry hostname/IP for deployment utility images',
                        callback=callback)(f)


def docker_namespace_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.docker_config.set_docker_namespace(value)
        return value

    return click.option('--docker-namespace',
                        is_eager=False,
                        expose_value=False,
                        help='Docker registry namespace for deployment utility images',
                        callback=callback)(f)


def deploy_profile_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.dart_env.tst_env.set_deploy_profile(value)
        return value

    return click.option('--deploy-profile',
                        is_eager=False,
                        expose_value=False,
                        help='Set the deployment profile used for provisioning/deployment.',
                        callback=callback)(f)


def project_id_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.dart_env.tst_env.set_project_id(value.lower())
        return value

    return click.option('--project-id',
                        is_eager=False,
                        expose_value=False,
                        help='Set the project id used for provisioning/deployment. (Can also be set with --dart-version [project_id]:[pipeline_version])',
                        callback=callback)(f)


def pipeline_version_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value is not None:
            state.dart_env.tst_env.set_pipeline_version(value)
        return value

    return click.option('--pipeline-version',
                        is_eager=False,
                        expose_value=False,
                        help='Set the pipeline version used for provisioning/deployment. (Can also be set with --dart-version [project_id]:[pipeline_version])',
                        callback=callback)(f)


def query_metadata_option(f):
    def callback(ctx, param, value):
        state: DartContext = ctx.ensure_object(DartContext)
        if value:
            query_metadata(state)
        return value

    return click.option('--query-metadata',
                        'query_metadata',
                        expose_value=False,
                        flag_value=True,
                        default=False,
                        help='Query AWS to get DART environment configuration',
                        callback=callback)(f)


def dart_options(f):
    f = profile_option(f)
    f = env_option(f)
    f = use_default_env_option(f)
    f = use_tst_env_option(f)
    f = use_custom_env_option(f)
    f = remote_deployment_option(f)
    f = tst_user_option(f)
    f = diab_user_option(f)
    f = diab_dir_option(f)
    f = diab_version_option(f)
    f = local_deployment_option(f)
    f = aws_env_option(f)
    f = dart_secret_option(f)
    f = dart_login_option(f)
    f = dart_password_option(f)
    f = dart_username_option(f)
    f = use_dart_public_login_option(f)
    f = basic_password_option(f)
    f = basic_username_option(f)
    f = basic_auth_creds(f)
    f = dart_auth_option(f)
    f = basic_auth_option(f)
    f = no_auth_option(f)
    f = kafka_auth_option(f)
    f = kafka_password_option(f)
    f = kafka_username_option(f)
    f = dart_tenant_option(f)
    f = aws_profile_option(f)
    f = ssh_public_key_option(f)
    f = dart_version_option(f)
    f = docker_auth_option(f)
    f = docker_password_option(f)
    f = docker_username_option(f)
    f = docker_registry_option(f)
    f = docker_namespace_option(f)
    f = deploy_profile_option(f)
    f = project_id_option(f)
    f = pipeline_version_option(f)
    f = query_metadata_option(f)
    return f
