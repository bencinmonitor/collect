# -*- coding:utf-8 -*-

import re
from json import loads
from ocr_machine.ocr import ocr_pipeline
from utils.meta import PETROL_FUEL_NAMES, OMV_FUEL_NAMES, FUEL_NAMES, FUEL_CODES, REVERSED_FUEL_CODES
from os.path import realpath, dirname, join, exists
from pprint import pprint
from redis import from_url
from datetime import datetime
from collector.settings import REDIS_DATA_URL
from utils.dict import flatten_dict

r = from_url(REDIS_DATA_URL)


def process_station(station_as_string):
    station = loads(station_as_string, encoding='utf8')
    prices = compute_prices(station)

    station['prices'] = prices
    save_station(station)

    return prices


def save_station(station):
    key = station['key']
    name = station['name']
    scraped_at = station['scraped_at']
    timestamp = int(datetime.strptime(scraped_at, '%Y-%m-%d %H:%M:%S').timestamp())

    # pprint(station)

    # 1. Current / Meta
    r.hmset('stations:meta:%s' % key, flatten_dict({
        'key': key,
        'name': name,
        'address': station['address'],
        'xcode': station['xcode'],
        'xid': station['xid'],
        'prices': {FUEL_CODES[k]: v for k, v in station['prices'].items()},
        'lat': station['lat'],
        'lon': station['lon'],
        'scraped_at': timestamp,
        'scraped_url': station['scraped_url']
    }, separator=":"))

    # Prices
    for price_name, value in station['prices'].items():
        price_code = FUEL_CODES[price_name]
        r.zadd("stations:prices:%s:%s" % (key, price_code), value, timestamp)

    # Price at location
    r.execute_command("GEOADD", "locations", station['lat'], station['lon'], key)

def fix_image_path(path):
    images_path = join(dirname(dirname(realpath(__file__))), "data")
    final_path = path

    if path.startswith("full/"):
        final_path = join(images_path, path)

    if not exists(final_path):
        raise Exception('Image path %s does NOT exist!' % final_path)

    return final_path


def compute_prices(station):
    result = ocr_pipeline([fix_image_path(image['path']) for image in station['images']])
    prices_list = [process_prices(station, out_text['out_text']) for out_text in result]
    prices = {k: v for d in prices_list for k, v in d.items()}
    return prices


def process_prices(station, text):
    if station['scraper'] == "petrol":
        return process_petrol_prices(station, text)
    elif station['scraper'] == "omv":
        return process_omv_prices(station, text)
    else:
        raise Exception('Processing of "%s" is not yet supported.' % station['scraper'])


def process_petrol_prices(station, text, names=PETROL_FUEL_NAMES):
    prices = [float(x.replace(",", ".", 1)) for x in re.findall(r"(\d{1},\d{3,3})", text)]
    labels = [k for k, (pattern, flags) in names if re.search(pattern, text, flags)]
    result = dict(zip(labels, prices))
    return result


def process_omv_prices(station, text, names=OMV_FUEL_NAMES):
    prices = [float(x.replace(",", ".", 1)) for x in re.findall(r"(\d{1},\d{3,3})", text)]
    labels = [k for k, (pattern, flags) in names if re.search(pattern, text, flags)]

    if len(labels) != len(prices):
        print("Station %s" % station['name'])
        print('Problem with "%s"' % (text))
        print("Lengths: %d %d" % (len(labels), len(prices)))
        print("Prices:", prices)
        print("Labels:", labels)
        return {}

    result = dict(zip(labels, prices))
    return result
