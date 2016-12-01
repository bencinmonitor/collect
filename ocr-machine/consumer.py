import argparse
from kafka import KafkaConsumer
from collector.settings import *
from PIL import *
from PIL import Image, ImageFilter
import tesserocr
from tesserocr import PyTessBaseAPI, PSM
import re
import threading, logging, time


class Consumer(threading.Thread):
    daemon = True

    def run(self):
        consumer = KafkaConsumer(KAFKA_SCRAPED_ITEMS_TOPIC, **{
            'bootstrap_servers': KAFKA_BOOTSTRAP_SERVERS,
            'group_id': 'ocr'
        })

        for msg in consumer:
            print(msg)


def main():
    threads = [Consumer()]
    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="Image to use instead of stream", type=str)
    args = parser.parse_args()

    main()
