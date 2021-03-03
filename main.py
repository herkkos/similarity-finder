# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 02:41:45 2021

@author: Herkko
"""

# Basic command line interface for using image similarity finder

import argparse
from spatial_similarity import SpatialSimilarity

parser = argparse.ArgumentParser(description='Welcome to similarity finder!')
parser.add_argument('folder', type=ascii, nargs=1, help='Source folder of images')
parser.add_argument('output file', type=ascii, nargs=1, help='Destination for output file')
parser.add_argument('-t', '--type', type=int, nargs=1, help='Type of similarity search')
parser.add_argument('-s', '--threshold', type=float, help='Threshold for similarity')
parser.add_argument('-f', '--filetypes', type=ascii, help='Filetypes to scan')
THRESHOLD = None
FILETYPES = None

args = parser.parse_args()
if args.threshold:
    THRESHOLD = args.threshold
if args.filetypes:
    FILETYPES = args.filetypes
if args.folder and args.output:
    if args.type:
        if args.type == 'spatial':
            # Call for spatial similarity
            print('Calling spatial similarity')
            SpatialSimilarity(args.folder, args.output, THRESHOLD, FILETYPES)
        elif args.type == 'freq':
            # Call for frequence based similarity
            print('TODO')
    else:
        # Call for spatial similarity
        print('Calling spatial similarity')
        SpatialSimilarity(args.folder, args.output, THRESHOLD, FILETYPES)
