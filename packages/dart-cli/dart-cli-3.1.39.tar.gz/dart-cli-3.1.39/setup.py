import json

from setuptools import setup, find_packages

setup_data_file = open('setup_data.json', 'rt')
setup_data = json.loads(setup_data_file.read())
setup_data_file.close()

tests_require = [
    'pytest',
    'mock',
    'moto',
]

install_requires = [
    'click',
    'pytest',
    'boto3',
    'botocore',
    'requests',
    'docker',
    'dockerpty',
    'pyjwt',
    'kafka-python',
]

setup(
    name=setup_data['name'],
    version=setup_data['version'],
    description='Data Acquisition and Reason Toolkit (DART) command-line interface',
    long_description='dart-cli provides a command-line interface for all of DART\'s REST services, as well as a host of other utilities related to deployment and debugging.',
    author='John Hungerford',
    author_email='john.hungerford@twosixtech.com',
    url="https://github.com/twosixlabs-dart/dart-cli",
    package_dir={'': 'src'},
    packages=find_packages('src'),
    py_modules=['dart', 'common_options', 'dart_context'],
    entry_points=f'''
        [console_scripts]
        {setup_data['cmd']}=cli.dart:cli
    ''',
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    tests_require=tests_require,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3.9",
    ],
)
