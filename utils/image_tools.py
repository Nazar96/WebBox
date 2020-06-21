import cv2
from shapely.geometry import Polygon
import numpy as np
import json


def create_heatmap(img_base, img_aug, thresh=1, ksize=(3, 3)):
    diff = img_base - img_aug
    diff = cv2.threshold(diff, thresh, 255, cv2.THRESH_BINARY)[1]
    diff = cv2.GaussianBlur(diff, ksize, cv2.BORDER_DEFAULT)
    return diff


def create_bbox(img_base, img_aug, thresh=130, ksize=(3, 3)):
    diff = create_heatmap(img_base, img_aug, thresh, ksize)
    contours = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    pols = []
    for c in contours:
        try:
            pols.append(Polygon(np.asarray(c).reshape(-1, 2)))
        except ValueError:
            pass
    return pols


def save_bbox(pols, path):
    result_path = path + '.json'
    bbox_list = [{'box': pol.bounds} for pol in pols]
    bbox_dict = {
        'form': {
            'words': bbox_list
        }
    }
    with open(result_path, 'w') as f:
        json.dump(bbox_dict, f)
    return result_path


def save_heatmap(heatmap, path):
    result_path = path + '.png'
    cv2.imwrite(result_path, heatmap)
    return result_path
