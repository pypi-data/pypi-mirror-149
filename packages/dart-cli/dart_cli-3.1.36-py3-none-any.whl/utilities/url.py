import re


def get_base_url(service: str, context: 'DartContext'):
    return context.dart_env.service_base_url(service)


def get_instance(service: str, context: 'DartContext'):
    return context.dart_env.service_instance(service)


def get_host(instance: str, context: 'DartContext'):
    return context.dart_env.instance_host(instance)

