import tempfile
import uuid
from time import sleep

import numpy as np
from skimage.measure import compare_ssim
from skimage.metrics import structural_similarity

import cv2
import selenium
from selenium import webdriver
from itertools import chain

from tqdm.autonotebook import tqdm
import os

from shapely.geometry import MultiPolygon, Polygon
import json


tags = ['p', 'h1', 'h2', 'h3', 'tr', 'th',]

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("window-size=1400,700")

def create_bbox(img_base, img_aug, thresh = 130,ksize=(5,5)):
    diff = (img_aug - img_base)
    diff = cv2.threshold(diff, thresh, 255, cv2.THRESH_BINARY)[1]
    diff = cv2.GaussianBlur(diff, ksize, cv2.BORDER_DEFAULT)
    contours = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    pols = []
    for c in contours:
        try:
            pols.append(Polygon(np.asarray(c).reshape(-1, 2)))
        except ValueError:
            pass

    pols = MultiPolygon(pols)
    return pols


class WebBoxGenerator():
    
    def __init__(self, options=options, path='./', links=[], tags=tags, sleep_time=0.5):
        
        self.screenshot_path = os.path.join(path, 'dataset/screenshots')
        self.annotation_path = os.path.join(path, 'dataset/annotations')
        
        for path in [self.screenshot_path, self.annotation_path]:
            os.makedirs(path, exist_ok=True)
                
        print(f'Screenshots in {self.screenshot_path}')
        print(f'Annotations in {self.annotation_path}')
        
        self.tags = tags
        self.links = links
        self.sleep_time = sleep_time
        
        self.driver_base = webdriver.Chrome(options=options)
        self.driver_aug = webdriver.Chrome(options=options)
    
    def __del__(self):
        self.driver_base.quit()
        self.driver_aug.quit()
    
    def generate_dataset(self):
        tmp_dir = tempfile.TemporaryDirectory()
        aug_path = os.path.join(tmp_dir.name, 'tmp.png')
        
        for url in tqdm(self.links):
            name = str(uuid.uuid4())
            img_path = os.path.join(self.screenshot_path, name+'.png')
            annot_path = os.path.join(self.annotation_path, name+'.json')

            self.driver_base.get(url)
            self.driver_aug.get(url)
            
            sleep(self.sleep_time)
                
            for tag in self.tags:
                for element in self.driver_aug.find_elements_by_tag_name(tag):
                    self.driver_aug.execute_script(f"arguments[0].style.opacity = 0.1", element)

            self.driver_base.save_screenshot(img_path)
            self.driver_aug.save_screenshot(aug_path)

            img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2GRAY)
            aug = cv2.cvtColor(cv2.imread(aug_path), cv2.COLOR_BGR2GRAY)

            pols = create_bbox(img, aug)

            bbox_dict = {}
            for i, pol in enumerate(pols):
                bbox_dict[f'box_{i}'] = pol.bounds

            with open(annot_path, 'w') as f:
                json.dump(bbox_dict, f)
            
        tmp_dir.cleanup()
        
    
    def add_links(self, links=[]):
        self.links = links
    
