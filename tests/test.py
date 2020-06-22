from webbox.webbox_generator import WebBoxGenerator
import unittest
import os
import shutil
from pathlib import Path


class TestWebBox(unittest.TestCase):
    def setUp(self):
        self.screen_path = './data/image/'
        self.markup_path = './data/annot/'

        shutil.rmtree(self.screen_path, ignore_errors=True)
        shutil.rmtree(self.markup_path, ignore_errors=True)

        Path(self.screen_path).mkdir(parents=True, exist_ok=True)
        Path(self.markup_path).mkdir(parents=True, exist_ok=True)

        self.wbg = WebBoxGenerator(
            screen_path=self.screen_path,
            markup_path=self.markup_path,
            sleep_time=0.1,
        )

        with open('./tests/links.txt', 'r') as f:
            self.links = [line.strip() for line in f.readlines()]

    def tearDown(self):
        shutil.rmtree(self.screen_path, ignore_errors=True)
        shutil.rmtree(self.markup_path, ignore_errors=True)

    def test_heatmap_generator(self):
        self.wbg.generate(self.links, 'heatmap')

        self.assertEqual(
            len(os.listdir(self.screen_path)),
            len(os.listdir(self.markup_path)),
            "Different number of files in screen and markaup directories"
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
