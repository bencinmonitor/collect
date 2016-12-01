# -*- coding: utf-8 -*-
from scrapy.utils.serialize import ScrapyJSONEncoder
from collector.settings import *
from json import dumps
from collector.items import Station
import threading, logging, time

from redis import Redis, from_url
from rq import Queue

from ocr_machine.processor import process_station


class StationsRedisPipeline(object):
    queue = None

    def open_spider(self, spider):
        self.queue = Queue(REDIS_ITEMS_QUEUE, connection=from_url(REDIS_URL))

    def process_item(self, item, spider):
        item_as_json = dumps(item, cls=ScrapyJSONEncoder)
        self.queue.enqueue(process_station, item_as_json)
