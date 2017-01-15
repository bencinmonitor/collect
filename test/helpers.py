import re, glob
from json import dumps
from scrapy.utils.serialize import ScrapyJSONEncoder

STATION_IMAGES = ['omv.jpg',
                  'omv-small.jpg',
                  'omv-three.jpg',
                  'petrol.jpg',
                  'petrol-bigger.jpg',
                  'petrol-bigger-2.jpg']


def build_station(options=None):
    if options is None:
        options = {}

    defaults = {
        "key": "petrol-1720-CE-MB",
        "xcode": "CE-MB",
        "scraped_url": "http://www.petrol.si/bencinski-servisi/podrobno/1720",
        "images": [{
            "url": "http://www.petrol.si/sites/www.petrol.si/files/bencinskiServisi/a7e354bd7861e271ceb965c4d65af4f0.jpg",
            "checksum": "47a778de507f7413c419371e0620a214",
            "path": "../data-test/petrol.jpg"}],
        "image_urls": [
            "http://www.petrol.si/...d65af4f0.jpg"
        ],
        "name": "BS Ptuj - Ormoška 26/b",
        "scraped_at": "2016-12-01 10:23:33",
        "scraper": "petrol",
        "address": "Ormoška cesta 26b, 2250 Ptuj",
        "lat": 46.41676013,
        "lon": 15.88049476,
        "xid": "1720",
        'services': {'caj_na_poti': 1,
                     'euroshell': 1,
                     'wifi': 1},
        'services_humans': {'caj_na_poti': 'Čaj na poti',
                            'euroshell': 'Euroshell',
                            'uta': 'UTA',
                            'wifi': 'WIFI'},
        'shopping_hours': {'friday': {'close': 2200, 'open': 600},
                           'monday': {'close': 2200, 'open': 600},
                           'saturday': {'close': 2200, 'open': 600},
                           'sunday': {'close': 2200, 'open': 800},
                           'thursday': {'close': 2200, 'open': 600},
                           'tuesday': {'close': 2200, 'open': 600},
                           'wednesday': {'close': 2200, 'open': 600}},
        'shopping_hours_humans': {'nedelje in prazniki': '8:00 - 22:00',
                                  'sobote': '6:00 - 22:00',
                                  'vsak delavnik': '6:00 - 22:00'},
    }
    return {**defaults, **options}


def station_as_json(station):
    return dumps(station, cls=ScrapyJSONEncoder, ensure_ascii=False)


def key_from_string(text):
    return re.sub(r'\W+', '-', text.lower())


def stations(glob_expression='./data-test/*.jpg', options=None):
    if options is None:
        options = {}

    return [build_station({**options, **{
        'key': key_from_string("test-%s" % image_path),
        'images': [{'path': image_path}]
    }}) for image_path in glob.glob(glob_expression)]
