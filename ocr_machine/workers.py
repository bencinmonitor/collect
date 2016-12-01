import sys
from collector.settings import REDIS_URL, REDIS_ITEMS_QUEUE
from redis import from_url
from rq import Connection, Worker
from logging import *

from ocr_machine.processor import process_station

if __name__ == '__main__':
    with Connection(from_url(REDIS_URL)):
        qs = sys.argv[1:] or ['default']

        w = Worker(qs)
        w.work(logging_level="DEBUG")
