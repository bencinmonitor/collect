# -*- coding: utf-8 -*-
from scrapy.utils.serialize import ScrapyJSONEncoder
from collector.settings import *
from kafka import KafkaProducer
from json import dumps
from collector.items import Station
import threading, logging, time


class StationsKafkaPipeline(object):
    producer = None

    def open_spider(self, spider):
        logging.basicConfig(level=logging.INFO)

        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: v.encode(),
            ssl_check_hostname=False,
            # compression_type='gzip'
        )

    def process_item(self, item, spider):
        key = Station.generate_key()
        item.setdefault('key', str(key))

        item_as_json = dumps(item, cls=ScrapyJSONEncoder)
        self.producer.send(KAFKA_SCRAPED_ITEMS_TOPIC, key=key.bytes, value=item_as_json)
        return item
