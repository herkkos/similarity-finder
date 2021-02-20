# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 12:47:42 2020

@author: Herkko
"""

import cv2
import imagehash
import itertools
import json
import numpy as np
import os

FILETYPES = ['.jpg', '.JPG', '.png', '.PNG', 'jpeg', 'JPEG']
FOLDER = r'TODO'
OUTPUT = r'TODO'
THRESHOLD = 1


# TODO: Convert this to a Java-style class with main 

# Returns 2D list
#   1d - image instance
#   2d - all files of the same instance
# THRESHOLD parameter determines how similar images need to be
def findSimilarity(images, THRESHOLD=1):
    similarOnes = np.array([])
    for a, b in itertools.combinations(images, 2):
        similarity = a[1] - b[1]
        # TODO: implement some kind of normalization for similarity and implement threshold
        if similarity == 0:
            similarOnes = np.append(similarOnes, (a[0], b[0]))
    return similarOnes.reshape(int(similarOnes.size / 2), 2)
    

# Loads all filenames into an array
def getFiles(folders):
    r = []
    for folder in folders:
        for root, dirs, files in os.walk(folder):
            for name in files:
                if name[-4:] in FILETYPES:
                    r.append(os.path.join(root,name))
    return r            

# Loads file and returns a hash which summarizes the image contents
def loadFile(file):
    im = cv2.imread(file, 0)
    im = cv2.resize(im, (32, 32), interpolation=cv2.INTER_LINEAR)
    im = imagehash.Image.fromarray(im)
    imhash = imagehash.dhash(im, 32)
    return imhash

# Returns a 2D numpy array of tuples containing imagehash and filepath
def scan(files):
    imageArray = np.array([])
    for file in files:
        imageArray = np.append(imageArray, [file, loadFile(file)])
    imageArray = imageArray.reshape(int(imageArray.size / 2), 2)
    return imageArray

# Writes similarities in output json file
# array contains numpy list of combinations of similar images
# OUTPUT is name or path for the output file
# TODO: smart implementation to go through all containing values
def writeToJSON(array, OUTPUT):
    data = {}
    for pair in array:
        if pair[0] in data:
            data[pair[0]].append(pair[1])
        elif pair[1] in data:
            data[pair[1]].append(pair[0])
        else:
            data[pair[0]] = []
            data[pair[0]].append(pair[1])
           
    with open(OUTPUT, 'w') as outfile:
        json.dump(data, outfile)

def main():
    imageFiles = getFiles([FOLDER])
    imageList = scan(imageFiles)
    similarOnes = findSimilarity(imageList)
    writeToJSON(similarOnes, OUTPUT)
    
    return 0
