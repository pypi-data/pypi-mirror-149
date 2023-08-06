import ssl
import threading

from dart_context.dart_context import DartContext
from utilities.url import get_host
import kafka
import ssl


class KafkaIntegration:
    def __init__(self, dart_context: DartContext):
        streaming_hostname = get_host('streaming', dart_context)
        bootstrap_servers = [f'{streaming_hostname}:9092']
        kafka_props = dart_context.kafka_config.kafka_props()
        kafka_props['bootstrap_servers'] = bootstrap_servers
        self.kakfa_props = kafka_props

    def consumer(self, topics: list[str], app_id, auto_offset_reset, enable_auto_commit):
        for topic in topics:
            print(topic)

        kafka_props = self.kakfa_props.copy()
        kafka_props['group_id'] = app_id
        kafka_props['auto_offset_reset'] = auto_offset_reset
        kafka_props['enable_auto_commit'] = enable_auto_commit
        return kafka.KafkaConsumer(*topics,
                                   **kafka_props)


def process_messages(consumer: kafka.KafkaConsumer, handle_record):
    for msg in consumer:
        key = msg.key.decode('utf-8')
        value = msg.value.decode('utf-8')
        handle_record(key, value)


def process_messages_in_thread(consumer: kafka.KafkaConsumer, handle_record):
    process_thread = threading.Thread(target=lambda: process_messages(consumer, handle_record))
    process_thread.start()
    return process_thread
