import time
from kafka import KafkaConsumer

SERVER = ['121.196.16.204:9091','121.196.16.204:9092','121.196.16.204:9093']
TOPIC = 'rpa-message'
print(("kafka server is {},topic is [{}]".format(SERVER, TOPIC)))
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=SERVER,
    group_id='rpa-worker',
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    consumer_timeout_ms=3 * 1000,
    # max_poll_interval_ms= 50*60*1000,
    # max_poll_records = 100

)


while 1:
    try:
        message = next(consumer)
        consumer.commit()
        print(message)
    except StopIteration:
        time.sleep(.5)