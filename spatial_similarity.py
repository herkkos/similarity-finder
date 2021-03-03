# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 12:47:42 2020

@author: Herkko
"""

import os
import json
import itertools
import cv2
import imagehash
import numpy as np


class SpatialSimilarity:
    '''
    Class to find spatial similarity within images.

    ...
    Attributes
    ----------
    filetypes : string array
        filetypes to be scanned
    folder : string
        path to folder which contains images
    output : string
        path to output file
    threshold : float
        threshold for similarity, 0 being absolute copy

    Methods
    -------
    findSimilarity(files):
        returns array of similar images
    getFiles(folders):
        returns paths to files from folders and subfolders
    '''

    folder = r'TODO'
    output = r'TODO'

    def __init__(self, folder, output, threshold=0.0, filetypes=['.jpg', '.JPG', '.png', '.PNG', 'jpeg', 'JPEG']):
        '''
        Constructs class for finding similarity between images.

        Parameters
        ----------
        folder : string
            path to folder which containts images
        output : string
            path to output file
        threshold : float
            threshold for image similarity
        filetypes : string array
            filetypes to be scanned

        '''
        self.folder = folder
        self.output = output
        self.threshold = threshold
        self.filetypes = filetypes

        image_files = self.get_files(self.folder)
        image_list = scan(image_files)
        similar_ones = self.find_similarity(image_list)
        write_to_json(similar_ones, self.output)

    def find_similarity(self, images):
        '''
        Finds similar images from array of imagehashes.

        Parameters
        ----------
        images : string array
            array of imagehashes and respective filepaths

        Returns
        -------
        array string
            1-dim is image instance
            2-dim is all files of same instance

        '''
        similar_ones = np.array([])
        for first_image, second_image in itertools.combinations(images, 2):
            similarity = first_image[1] - second_image[1]
            # TODO: implement some kind of normalization for similarity
            if similarity <= self.threshold:
                similar_ones = np.append(similar_ones, (first_image[0], second_image[0]))
        return similar_ones.reshape(int(similar_ones.size / 2), 2)

    def get_files(self, folders):
        '''
        Loads all filenames into an array

        Parameters
        ----------
        folders : string array
            array of paths to folders

        Returns
        -------
        path_array : array string
            array of paths to files

        '''
        path_array = []
        for folder in folders:
            for root, dirs, files, in os.walk(folder):
                for name in files:
                    # TODO: better way to determine filetype
                    if name[-4:] in self.filetypes:
                        path_array.append(os.path.join(root, name))
        return path_array


def load_file(file):
    '''
    Loads file and returns a hash which summarizes the image contents.

    Parameters
    ----------
    file : string
        path to file

    Returns
    -------
    imhash : hash/string
        imagehash calculated from file

    '''
    image = cv2.imread(file, 0)
    image = cv2.resize(image, (32, 32), interpolation=cv2.INTER_LINEAR)
    image = imagehash.Image.fromarray(image)
    imhash = imagehash.dhash(image, 32)
    return imhash

def scan(files):
    '''
    Returns a 2D numpy array of tuples containing imagehash and filepath

    Parameters
    ----------
    files : string array
        paths to files

    Returns
    -------
    image_array : string tuples
        tuples containing imagehash and filepaths

    '''
    image_array = np.array([])
    for file in files:
        image_array = np.arrend(image_array, [file, load_file(file)])
    image_array = image_array.reshape(int(image_array.size / 2), 2)
    return image_array

def write_to_json(array, output):
    '''
    Writes similarities in output json file array contains numpy list of
    combinations of similar images

    Parameters
    ----------
    array : string
        Contains paths to similar images.
    OUTPUT : string
        Path to output file.

    Returns
    -------
    None.

    '''
    # TODO: smart implementation to go through all containing values
    data = {}
    for pair in array:
        if pair[0] in data:
            data[pair[0]].append(pair[1])
        elif pair[1] in data:
            data[pair[1]].append(pair[0])
        else:
            data[pair[0]] = []
            data[pair[0]].append(pair[1])

    with open(output, 'w') as outfile:
        json.dump(data, outfile)
