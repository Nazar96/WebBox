import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from tqdm.autonotebook import tqdm
from uuid import uuid4
from time import sleep
import numpy as np
from tempfile import TemporaryDirectory
import cv2
from utils import func


class WebBoxGenerator:
    def __init__(self, screen_path='./data/image/', sleep_time=0.5, markup_path='./data/annot/', headless=True):
        self.headless = headless
        self.screen_path = screen_path
        self.markup_path = markup_path if markup_path is None else markup_path
        self.sleep_time = sleep_time

        self.modification_script = """
        elements = document.querySelectorAll('*')
        for (var i=0; i<elements.length; i++){
            elements[i].style.color = 'rgba(0,0,0,0)'
        }
        """

    @staticmethod
    def __save_result(method, img_base, img_aug, path):
        result = func[method][0](img_base, img_aug)
        func[method][1](result, path)

    def __create_anchors(self, driver, max_anchors):
        page_height = driver.execute_script("return document.body.scrollHeight")
        window_height = driver.get_window_size()['height']

        if max_anchors is None:
            max_anchors = max(1, page_height // window_height)

        anchors = np.random.randint(max(page_height - window_height, 0), size=max_anchors)
        return anchors

    def generate(self, url_list, method='heatmap', max_anchors=None):
        options = Options()
        options.headless = self.headless
        driver = webdriver.Firefox(options=options)
        # driver set options
        try:
            for url in tqdm(url_list):
                tmp_dir = TemporaryDirectory()
                image_name = str(uuid4())

                screen_path = os.path.join(self.screen_path, image_name)
                tmp_path = os.path.join(tmp_dir.name, image_name)
                markup_path = os.path.join(self.markup_path, image_name)

                driver.get(url)
                sleep(self.sleep_time)

                anchors = self.__create_anchors(driver, max_anchors)

                # create original screenshots:
                for anchor in anchors:
                    driver.execute_script(f'window.scrollTo(0, {anchor})')
                    driver.save_screenshot(screen_path+'_'+str(anchor)+'.png')

                # create modified screenshots
                driver.execute_script(self.modification_script)
                for anchor in anchors:
                    orig_path = screen_path+'_'+str(anchor)+'.png'
                    mod_path = tmp_path+'_'+str(anchor)+'.png'

                    driver.execute_script(f'window.scrollTo(0, {anchor})')
                    driver.save_screenshot(mod_path)

                    # create markup
                    orig_img = cv2.cvtColor(cv2.imread(orig_path), cv2.COLOR_BGR2GRAY)
                    mod_img = cv2.cvtColor(cv2.imread(mod_path), cv2.COLOR_BGR2GRAY)
                    self.__save_result(method, orig_img, mod_img, markup_path+str(anchor))

                tmp_dir.cleanup()

        finally:
            driver.quit()
