import glob
import unittest

from ocr_machine.ocr import *
from test.helpers import build_station, stations


class ProcessorTest(unittest.TestCase):
    def test_building_payload(self):
        station = build_station({'xid': "test"})
        self.assertEqual(station['xid'], "test")

    def test_pre_process(self):
        for station in stations():
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

        for node in post_process_results:
            # print('"%s"' % node['out_text'])
            self.assertRegex(node['out_text'], r"\d{1},\d{3,3}")
        self.assertEqual(len(nodes), 6)


if __name__ == '__main__':
    unittest.main()
