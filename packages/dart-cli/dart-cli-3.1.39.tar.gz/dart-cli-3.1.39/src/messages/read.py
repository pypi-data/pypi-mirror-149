import uuid

import click

from cli import global_options
from dart_kafka.kafka_integration import KafkaIntegration, process_messages_in_thread
from dart_kafka.message_printer import SimpleMessagePrinter, JsonMessagePrinter


@click.command(name='read')
@global_options.dart_options
@click.option('--key/--no-key',
              required=False,
              default=True,
              help='Print message key')
@click.option('--value/--no-value',
              required=False,
              default=True,
              help='Print full message')
@click.option('-o',
              '--output',
              type=click.File('w'),
              required=False,
              default=None,
              help='Specify target file to write output')
@click.option('--id',
              'app_id',
              required=False,
              default=None,
              help='Set app id (allows to consume from last point)')
@click.option('--from-now/--from-beginning',
              required=False,
              default=False,
              help='Read messages starting from oldest (default) or from present time. (Only if app_id is new.)')
@click.option('--incl',
              help='Provide path to include if message is in JSON format. Can be used multiple times to include multiple fields. Format: key.nested_key.nested_nested_key ... etc',
              multiple=True,
              default=[])
@click.option('--excl',
              help='Provide path to exclude if message is in JSON format. Can be used multiple times to include multiple fields. Format: key.nested_key.nested_nested_key ... etc',
              multiple=True,
              default=[])
@click.option('--filter-empty',
              is_flag=True,
              help='Filter out messages with empty values (either empty string or empty json)',
              required=False)
@click.argument('topic',
                nargs=1,
                required=True)
@global_options.pass_dart_context
def read_command(dart_context,
                 key: bool,
                 value: bool,
                 output,
                 app_id,
                 from_now,
                 incl: list[str],
                 excl: list[str],
                 filter_empty: bool,
                 topic):
    """Check the status of DART services"""

    app_id_final = str(uuid.uuid1())
    if app_id is not None:
        app_id_final = app_id
    auto_offset = 'earliest'
    if from_now:
        auto_offset = 'latest'
    simple_printer = SimpleMessagePrinter(key, value, filter_empty, output)
    printer = simple_printer
    if len(incl) > 0 or len(excl) > 0:
        printer = JsonMessagePrinter(incl, excl, simple_printer)
    kakfa_integration = KafkaIntegration(dart_context)
    consumer = kakfa_integration.consumer([topic], app_id_final, auto_offset, False)
    process_messages_in_thread(consumer, printer.print_message)
