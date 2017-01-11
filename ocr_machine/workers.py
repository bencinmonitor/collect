import sys
from collector.settings import REDIS_URL, MONGO_URL
from redis import from_url
from rq import Connection, Worker
from os import getenv

if __name__ == '__main__':
    with Connection(from_url(REDIS_URL)):
        qs = sys.argv[1:] or ['default']
        w = Worker(qs)
        w.work(logging_level=getenv('LOG_LEVEL', 'DEBUG'))
