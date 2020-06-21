import os
from selenium import webdriver
from tqdm.autonotebook import tqdm
from uuid import uuid4
from time import sleep
import numpy as np
import tempfile
import cv2


class WebBoxGenerator():
    def __init__(self, screen_path, sleep_time=0.5, markup_path=None, max_anchors=None):
        self.screen_path = screen_path
        self.markup_path = markup_path if markup_path is None \
            else self.markup_path = markup_path
        self.sleep_time = sleep_time
        self.max_anchors = max_anchors

        self.modification_script = """
        elements = document.querySelectorAll('*')
        for (var i=0; i<elements.length; i++){
            elements[i].style.color = 'rgba(0,0,0,0)'
        }
        """

    def __create_anchors(self, driver):
        page_height = driver.execute_script("return document.body.scrollHeight")
        window_height = driver.get_window_size()['height']

        if self.max_anchors is None:
            max_anchors = max(1, page_height // window_height)
        else:
            max_anchors = self.max_anchors

        anchors = np.random.randint(max(page_height - window_height, 0), size=max_anchors)
        return anchors

    def generate(self, url_list):
        tmp_dir = tempfile.TemporaryFile()
        driver = webdriver.Firefox()
        # driver set options

        for url in tqdm(url_list):
            image_name = str(uuid4())
            screen_path = os.path.join(self.screen_path, image_name)
            tmp_path = os.path.join(tmp_dir.name, image_name)
            markup_path = os.path.join(self.markup_path, image_name)

            driver.get(url)
            sleep(self.sleep_time)

            anchors = self.__create_anchors(driver)

            # create original screenshots:
            for anchor in anchors:
                driver.execute_script(f'window.scrollTo(0, {anchor})')
                driver.save_screenshot(screen_path+'_'+str(anchor)+'.png')

            # create modified screenshots
            driver.execute_script(self.modification_script)
            for anchor in anchors:
                driver.execute_script(f'window.scrollTo(0, {anchor})')
                driver.save_screenshot(tmp_path+'_'+str(anchor)+'.png')

            # create markup:
            for anchor in anchors:
                orig_path = screen_path + '_' + str(anchor) + '.png'
                mod_path = tmp_path + '_' + str(anchor) + '.png'

                orig_img = cv2.cvtColor(cv2.imread(orig_path), cv2.COLOR_BGR2GRAY)
                mod_img = cv2.cvtColor(cv2.imread(mod_path), cv2.COLOR_BGR2GRAY)


