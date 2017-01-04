# -*- coding: utf-8 -*-

import unittest
import re, glob
from pprint import pprint
from test.helpers import build_station, stations, station_as_json
from ocr_machine.processor import process_station
from json import dumps
from scrapy.utils.serialize import ScrapyJSONEncoder


class TestProcessor(unittest.TestCase):
    def setUp(self):
        pass

    def test_processor_petrol(self):
        path = "./data-test/petrol*.jpg"
        path = "./data-test/petrol-bigger-2.jpg"
        # path = "./data/full/*.jpg"
        stations_data = [station_as_json(station) for station in stations(path)]
        results = [process_station(station) for station in stations_data]
        first_result = results[0]

        self.assertEqual(first_result['Q Max 95'], 1.206)
        self.assertEqual(first_result['Q Max 100'], 1.289)
        self.assertEqual(first_result['Q Max Diesel'], 1.110)

    def test_processor_omv(self):
        path = "./data-test/omv*.jpg"
        path = "./data-test/omv-complex*"
        stations_data = [station_as_json(station) for station in stations(path, options={'scraper': 'omv'})]
        results = [process_station(station) for station in stations_data]

        first_result = results[0]
        self.assertEqual(first_result['OMV Avtoplin (LPG)'], 0.613)
        self.assertEqual(first_result['OMV Diesel'], 1.110)

    def test_processor_with_merge(self):
        path = "./data-test/omv*.jpg"
        station = build_station({
            'scraper': 'omv',
            'images': [{'path': f_path} for f_path in glob.glob(path)]
        })

        station_json = station_as_json(station)
        prices = process_station(station_json)
        self.assertEqual(prices['OMV Diesel'], 1.110)

    def test_saving(self):
        path = "./data-test/petrol-bigger-2.jpg"
        station = station_as_json(build_station({
            'images': [{'path': f_path} for f_path in glob.glob(path)]
        }))

        prices_one = process_station(station)

        path = "./data-test/omv*.jpg"
        station = station_as_json(build_station({
            'scraper': 'omv',
            'key': 'some-omv-test',
            'name': 'some OMV',
            'images': [{'path': f_path} for f_path in glob.glob(path)]
        }))

        prices_two = process_station(station)


if __name__ == '__main__':
    unittest.main()
