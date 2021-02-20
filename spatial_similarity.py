# -*- coding: utf-8 -*-
"""
"""

import concurrent.futures
import itertools
import cv2
import multiprocessing
import numpy as np
from typing  import List
from config import ConfigManager
from data import DataManager

MAX_RES = 24

class SpatialSimilarity:

    def __init__(self, config : ConfigManager, data : DataManager):
        image_files = data.get_filepaths()
        image_array = scan(image_files)
        similar_ones = self.find_similarity(image_array, config.get_threshold())
        data.set_similars(similar_ones)
        data.write_to_json()

def find_similarity(self, image_array, threshold):
    similar_ones = np.array([])
    for first_image, second_image in itertools.combinations(image_array, 2):
        #TODO: more sophisticated way to calculate image similarity
        # Should be noted that this already implements pyramidic grid though
        # it could be imporved by changing the order of grid elements
        similarity = first_image[1].astype('int32') - second_image[1].astype('int32')
        similarity = np.abs(similarity.mean())
        if similarity <= threshold:
            similar_ones = np.append(
                similar_ones, (first_image[0], second_image[0]))
    return similar_ones.reshape(int(similar_ones.size / 2), 2)

def load_file(file):
    img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return np.array([])
    pyramid_data = []
    for i in range(1, MAX_RES+1):
        clone_img = img.copy()
        clone_img = cv2.resize(clone_img, (i,i))
        for a in clone_img.reshape(clone_img.size):
            pyramid_data.append(a) 
    return np.array(pyramid_data)

def scan(files : List):
    image_array = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count() - 1) as executor:
        futures = {executor.submit(load_file, file): file for file in files}
        for future in concurrent.futures.as_completed(futures):
            file = futures[future]
            data = future.result()
            if data.size == 0:
                continue
            image_array.append((file, data))
        
    return np.array(image_array)
