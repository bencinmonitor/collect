# -*- coding: utf-8 -*-
from scrapy.utils.serialize import ScrapyJSONEncoder
from collector.settings import *
from kafka import KafkaProducer
from json import dumps


class StationsKafkaPipeline(object):
    producer = None

    def open_spider(self, spider):
        self.producer = KafkaProducer(**{
            'bootstrap_servers': KAFKA_BOOTSTRAP_SERVERS,
            'value_serializer': lambda v: v.encode(),
        })

    def process_item(self, item, spider):
        item_as_json = dumps(item, cls=ScrapyJSONEncoder)
        self.producer.send(KAFKA_SCRAPED_ITEMS_TOPIC, item_as_json)
        return item
