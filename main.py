# -*- coding: utf-8 -*-
"""
Basic command line interface for using image similarity finder
"""


import argparse
from spatial_similarity import SpatialSimilarity
from config import ConfigManager
from data import DataManager


def parse_args():
    parser = argparse.ArgumentParser(description='Welcome to similarity finder!')
    parser.add_argument('folder', type=ascii, nargs=1, help='Source folder of images')
    parser.add_argument('output file', type=ascii, nargs=1, help='Destination for output file')
    parser.add_argument('-t', '--type', type=int, nargs=1, help='Type of similarity search')
    parser.add_argument('-s', '--threshold', type=float, help='Threshold for similarity')
    parser.add_argument('-f', '--filetypes', type=ascii, help='Filetypes to scan')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    
    config = ConfigManager()
    data = DataManager(config)

    if args.threshold:
        config.set_threshold(args.threshold)
    if args.filetypes:
        config.set_filetypes(args.filetypes)
    if args.folder:
        config.set_input_paths(args.folder)
    if args.output:
        config.set_output_path(args.output)
        
    if args.type and args.type == 'freq':
        print('TODO')
    else:
        print('Calling spatial similarity')
        SpatialSimilarity(config, data)


if __name__ == '__main__':
    main()

