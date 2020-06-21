from webbox.webbox_generator import WebBoxGenerator
import unittest
import os


class TestWebBox(unittest.TestCase):
    def setUp(self):
        self.screen_path = './data/image'
        self.markup_path = './data/annot'

        self.wbg = WebBoxGenerator(
            screen_path=self.screen_path,
            markup_path=self.markup_path,
            sleep_time=0.1,
        )

        with open('./test/links.txt', 'r') as f:
            self.links = [line.strip() for line in f.readlines()]

    def test_heatmap_generator(self):
        self.wbg.generate(self.links, 'heatmap')
        self.assertEqual(
            len(os.listdir(self.screen_path)),
            len(os.listdir(self.markup_path)),
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)

