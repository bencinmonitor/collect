import unittest
import glob
from pprint import pprint
import re

from ocr_machine.processor import *


class ProcessorTest(unittest.TestCase):
    station_images = ['omv.jpg',
                      'omv-small.jpg',
                      'omv-three.jpg',
                      'petrol.jpg',
                      'petrol-bigger.jpg',
                      'petrol-bigger-2.jpg']

    def key_from_string(self, text):
        return re.sub(r'\W+', '-', text.lower())

    def build_station(self, options={}):
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
            "name": "BS Ptuj - Ormo\\u0161ka 26/b",
            "scraped_at": "2016-12-01 10:23:33",
            "scraper": "petrol",
            "address": "Ormo\\u0161ka cesta 26b, 2250 Ptuj",
            "lat": 46.41676013,
            "lon": 15.88049476,
            "xid": "1720"
        }
        return {**defaults, **options}

    def stations(self):
        return [self.build_station({
            'key': self.key_from_string("test-%s" % image_path),
            'images': [{'path': image_path}]
        }) for image_path in glob.glob('./data-test/*.jpg')]

    def test_building_payload(self):
        station = self.build_station({'xid': "test"})
        self.assertEqual(station['xid'], "test")

    def test_pre_process(self):
        for station in self.stations():
            pre_process_result = pre_process([image['path'] for image in station['images']])
            self.assertEqual(1, len(pre_process_result))

    def test_ocr(self):
        images = [pre_process_image(file_path) for file_path in glob.glob('./data-test/*.jpg')[0:1]]
        texts = ocr(images)
        self.assertEqual(len(texts), 1)
        self.assertIn('Kurilno', texts[0]['text'])

    def test_post_process(self):
        images = [pre_process_image(file_path) for file_path in glob.glob('./data-test/*.jpg')]
        nodes = ocr(images)
        post_process_results = post_process(nodes, debug_numbers=True)

        # for node in post_process_results:
        #    print("--->")
        #    print(node['out_text'])

        self.assertEqual(len(nodes), 6)


if __name__ == '__main__':
    unittest.main()
