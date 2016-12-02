from json import loads, load
from ocr_machine.ocr import ocr_pipeline
import re


def process_station(station_as_json):
    if isinstance(station_as_json, (str)):
        station = loads(station_as_json, 'utf8')
    elif isinstance(station_as_json, dict):
        station = station_as_json
    else:
        raise Exception('Station can only be "hash" or "json"')

    result = ocr_pipeline([images['path'] for images in station['images']])
    out_texts = ' '.join([x['out_text'] for x in result])

    prices = process_prices(station, out_texts)

    return prices


def process_prices(station, text):
    if station['scraper'] is 'petrol':
        result = process_petrol_prices(station, text)
    elif station['scraper'] is 'omv':
        result = process_omv_prices(station, text)
    else:
        raise Exception('Processing of "%s" is not yet supported.' % station['scraper'])

    return result


PETROL_FUEL_NAMES = [
    ('Q Max 95', ("max 95", re.IGNORECASE)),
    ('Q Max 100', ("max 100", re.IGNORECASE)),
    ('Q Max Diesel', ("diesel", re.IGNORECASE)),
    ('Q Max LPG', ("LPG", re.IGNORECASE)),
    ('Kurilno olje EL', ("kurilno|olje", re.IGNORECASE))
]


def process_petrol_prices(station, text, names=PETROL_FUEL_NAMES):
    prices = [float(x.replace(",", ".", 1)) for x in re.findall(r"(\d{1},\d{3,3})", text)]
    labels = [k for k, (pattern, flags) in names if re.search(pattern, text, flags)]
    result = dict(zip(labels, prices))
    return result


OMV_FUEL_NAMES = [
    ('MaxxMotion 95', (r"(\b95\b|motion\s9)", re.IGNORECASE)),
    ('OMV AdBlue', (r"AdBlue|blue", re.IGNORECASE)),
    ('MaxxMotion 100', (r"(\b100\b|motion\s1)", re.IGNORECASE)),
    ('Kurilno olje OMV futurPlus', (r"kurilno|olje|futur|plus", re.IGNORECASE)),
    ('OMV Avtoplin (LPG)', (r"LPG|\W+plin", re.IGNORECASE)),
    ('OMV Diesel', (r"diesel", re.IGNORECASE)),
]

from pprint import pprint


def process_omv_prices(station, text, names=OMV_FUEL_NAMES):
    print('"%s' % text)
    prices = [float(x.replace(",", ".", 1)) for x in re.findall(r"(\d{1},\d{3,3})", text)]
    labels = [k for k, (pattern, flags) in names if re.search(pattern, text, flags)]

    if len(labels) != len(prices):
        print('Problem with "%s"' % (text), prices, labels)
        return {}

    result = dict(zip(labels, prices))
    return result
