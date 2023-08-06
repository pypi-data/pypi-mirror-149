# DART command-line interface

dart-cli provides a command-line interface for all of DART's REST services, as well as a host of other 
utilities related to deployment and debugging.

## Install

Requires python 3.8

In the project root, use the following command:

```bash
pip install .
```

## Basic Usage

Like aws-cli, git, and docker, dart-cli is built around commands and subcommands. Its syntax should be
familiar:
```shell script
dart command [subcommand] [...options] [...arguments]
  ...
dart forklift --input-dir ./raw_docs --labels "test upload"  # Upload documents for ingestion
dart reprocess --input-dir ./cdrs # upload cdrs for reprocessing
```

## Configuration

All configuration can provided via command-line arguments. Some configuration options that are common between DART
tools can be provided at any stage of the command. E.g.,
```shell script
dart --env --ssh-key ~/.ssh/id_rsa.pub provision ...
```
or
```shell script
dart provision --env wm --ssh-key ~/.ssh/id_rsa.pub ...
```
You can see all of these global configuration options by running `dart --help`.

### Deployment Environment

[TODO]

### Configuration Profiles

These global options can also be set in configuration files, each of which should have the form 
`~/.dart/[profile].conf`, where `[profile]` can be used to with the global command-line option `--profile [profile]`. 
The `--profile` option is always consumed first, so any configuration parameters set on the command line will
override the profile configuration regardless of the order.

Dart's configuration files should be in JSON format. The schema can be deduced from the `DartContext` class in
`src/dart_context.py` (see the methods `from_profile()` and `from_dict()`).

The `profiles` command group can be used to manage configuration profiles. Use `dart profiles ls` to see your
profiles, and `dart profiles view [profile]` to show their contents. `dart profiles add [profile]` will create
a new profile using whatever configuration has been set via the command line. So, e.g.,

```bash
$ dart --basic-login [basic-auth-un]:[basic-auth-pwd] \
       --dart-login [dart-un]:[dart-pwd] \
       --dart-secret [dart-cli-client-secret] \
       --docker-login [docker-un]:[docker-pwd] \
       --aws-profile [profilename] \
       --aws-environment dart \
       --ssh-key id_rsa \
       profiles add dart-profile

$ dart profiles view dart-profile
{
    "aws_profile": "[profilename]",
    "ssh_key": "id_rsa",
    "tenants": [],
    "dart_env": {
        "env_type": "default",
        "tst_env": {
            "aws_environment": "dart"
        },
        "custom_env": {
            "instance_mapping": {},
            "service_mapping": {}
        }
    },
    "auth_config": {
        "auth_type": "no_auth",
        "dart_auth": {
            "username": "[dart-un]",
            "password": "[dart-pwd]",
            "client_secret": "[dart-cli-client-secret]",
            "use_client_secret_flag": true
        },
        "basic_auth": {
            "username": "[basic-auth-un]",
            "password": "[basic-auth-pwd]"
        }
    },
    "kafka_config": {
        "config_type": "default"
    },
    "docker_config": {
        "docker_username": "[docker-un]",
        "docker_password": "[docker-pwd]"
    }
}
```

Since `dart profiles add` simply writes the current dart-cli configuration to a configuration profile, it is easy
to copy or "extend" an existing profile by selecting this profile with `-p` and then adding desired options:

```shell script
dart -p existing-profile [OPTIONS] profiles add new-profile
```

This will create a new profile based on `existing-profile` with parameters updated by whatever `CONFIGURATION OPTIONS`
you include. You can also update an existing profile by writing back to the same profile, e.g.,
```shell-script
dart -p existing-profile [OPTIONS] profiles add existing-profile
```

To view an updated configuration without saving it to a new profile, you can use the command `profiles view` without
specifying a profile:

```shell script
dart -p dart-profile \
     --basic-login ex-username:ex-password \
     profiles view
{
    "aws_profile": "[profilename]",
    "ssh_key": "id_rsa",
    "tenants": [],
    "dart_env": {
        "env_type": "default",
        "tst_env": {
            "aws_environment": "dart"
        },
        "custom_env": {
            "instance_mapping": {},
            "service_mapping": {}
        }
    },
    "auth_config": {
        "auth_type": "no_auth",
        "dart_auth": {
            "username": "[dart-un]",
            "password": "[dart-pwd]",
            "client_secret": "[dart-cli-client-secret]",
            "use_client_secret_flag": true
        },
        "basic_auth": {
            "username": "ex-username",
            "password": "ex-password"
        }
    },
    "kafka_config": {
        "config_type": "default"
    },
    "docker_config": {
        "docker_username": "[docker-un]",
        "docker_password": "[docker-pwd]"
    }
}
```

### Configuration workflow

By building on existing profiles in this way, you can easily generate new profiles for any dart environment. The following
is the recommended workflow for doing this.

#### 1. Global credentials

If you use any TST deployment configurations or custom deployment configurations that include authentication 
and authorization, you will probably want a separate profile to keep your credentials:

```shell script
dart --dart-login [username]:[password] \  # credentials for dart auth using public login flow
     --dart-secret [secret] \              # credentials for dart auth using dart-cli client secret
     --basic-login [username]:[password] \ # credentials for basic auth access when dart-auth is disabled
     --docker-login [username]:[password] \ # for running docker containers for provision/deploy
     --ssh-key id_rsa \                    # for running ansible and the ssh command necessary for TST-environment deployments
     profiles add credentials
```

#### 2. AWS environments

You will also want separate profiles for each of the two AWS accounts DART uses. Each of these should include the
credentials stored in the `credentials` profile above:

```shell script
dart -p credentials \                         # Inherit credentials configuration
     --aws-environment dart \                 # Set the dart-pipeline type that will be used for deployment
     --aws-profile [your-dart-profile-name]\  # Set the AWS profile name that will be used to access the appropraite AWS account
     profiles add dart                        # Create a new configuration profile with above configuration

dart -p credentials \
     --aws-environment prod \
     --aws-profile [your-prod-profile-name] \
     profiles add prod
```

#### 3. Env-specific profiles

Finally, you will want to generate profiles for each DART environment you want to interact with, so that you do
not have to continually use cli options to use its services.

To create a profile for an environment that *does not exist yet*, simply combine the env-specific configuration
properties with either the `dart` or `prod` profiles from above, depending on which account you intend to deploy
this DART environment in:

```shell script
dart -p dart \                           # Inherit configuration for dart AWS account and deployment environment
     --env dartenv \                     # Set environment name (i.e, dartenv.dart.worldmodelers.com)
     --deploy-profile dart-distributed \ # Set deployment profile, used by AWS cdk to determine services configuration
     --dart-version wm:2.0.64 \          # Set project id (e.g., wm-dart-pipeline or dev-dart-pipeline) and version (tag of docker image used for deployment)
     profiles add dartenv                # Create a new configuration profile with above configuration 
```

Note that we've named the profile after the DART environment (`dartenv`). This profile can now be used to provision
and deploy the pipeline:

```shell script
dart -p dartenv pipeline provision-deploy all 
```

To create a profile for an environment that *has already been deployed*, you can use the `--query-metadata` option
to pull the env-specific configuration from metadata stored in aws:

```shell script
dart -p dart \            # Inherit configuration
     --env dartenv \      # Set environment name
     --query-metadata \   # Pull deployment profile, project id, and version from AWS
     profiles add dartenv # Create a new profile with above configuration
```

### Local DART Environment

Set the `--local` flag to use DART services deployed locally. Currently, this can only be used for DART services
(e.g., corpex, forklift, reprocess, etc.) and not for provisioning or deployment.
