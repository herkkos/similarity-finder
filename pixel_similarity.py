# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 00:47:44 2021

@author: Herkko
"""

import os
import json
import itertools
import cv2
import numpy as np


class PixelSimilarity:
    '''
    Class to find pixel similarity within images.

    ...
    Attributes
    ----------
    filetypes : string array
        Filetypes to be scanned.
    folder : string
        Path to folder which contains images.
    output : string
        Path to output file.
    threshold : float
        Threshold for similarity, 0 being absolute copy.

    Methods
    -------
    findSimilarity(files):
        Returns array of similar images.
    getFiles(folders):
        Returns paths to files from folders and subfolders.
    '''

    def __init__(self, folder, output, threshold=0.0,
                 filetypes=['.jpg', '.JPG', '.png', '.PNG', 'jpeg', 'JPEG']):
        '''
        Constructs class for finding similarity between images using pixel comparisons.

        Parameters
        ----------
        folder : string
            Path to folder which contains images.
        output : string
            Path to output file.
        threshold : float, optional
            Threshold for similarity. The default is 0.0.
        filetypes : string array, optional
            Filetypes to be scanned. The default is ['.jpg', '.JPG', '.png', '.PNG', 'jpeg', 'JPEG'].

        Returns
        -------
        None.

        '''
        self.folder = folder
        self.output = output
        self.threshold = threshold
        self.filetypes = filetypes

        image_files = self.get_files(self.folder)
        image_list = scan(image_files)
        similar_ones = self.find_similarity(image_list)
        write_to_json(similar_ones, self.output)

    def find_similarity(self, imagelist):
        '''
        Finds similar images from array of imagehashes.

        Parameters
        ----------
        imagelist : string array
            Array of images and respective filepaths.

        Returns
        -------
        array string
            1-dim is image instance
            2-dim is all files of same instance

        '''
        similar_ones = np.array([])
        for first_image, second_image in itertools.combinations(imagelist, 2):
            similarity = first_image[1] - second_image[1]
            # TODO: Check this
            if similarity <= self.threshold:
                similar_ones = np.append(
                    similar_ones, (first_image[0], second_image[0]))
        return similar_ones.reshape(int(similar_ones.size / 2), 2)

    def get_files(self, folders):
        '''
        Loads all filenames into an array

        Parameters
        ----------
        folders : string array
            Array of paths to folders.

        Returns
        -------
        path_array : string array
            Array of paths to files.

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
        Path to file.

    Returns
    -------
    image : integer array
        Array of integers.

    '''

    image = cv2.imread(file, 0)
    image = cv2.resize(image, (32, 32), interpolation=cv2.INTER_LINEAR)
    image = cv2.convertScaleAbs(image)
    return image


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
