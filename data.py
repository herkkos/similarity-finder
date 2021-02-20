# -*- coding: utf-8 -*-
"""
"""

import json
from pathlib import Path
from typing  import List
from config import ConfigManager

class DataManager:

    __file_paths = None    
    __similar_paths = None
    
    def __init__(self, config : ConfigManager):
        self.allowed_types = config.get_filetypes()
        self.input_paths = config.get_input_paths()
        self.output_path = config.get_output_path()
        self.get_files()
    
    def get_filepaths(self):
        return self.__file_paths
    
    def get_files(self):
        path_array = []
        for folder in self.input_paths:
            for f_type in self.allowed_types:
                filetype = '*.' + f_type
                for file in Path(folder).rglob(filetype):
                    path_array.append(str(file.absolute()))
        self.__file_paths = path_array
    
    def set_similars(self, similars : List):
        self.__similar_paths = similars
    
    def write_to_json(self):
        # TODO: smart implementation to go through all containing values
        data = {}
        for pair in self.__similar_paths:
            if pair[0] in data:
                data[pair[0]].append(pair[1])
            elif pair[1] in data:
                data[pair[1]].append(pair[0])
            else:
                data[pair[0]] = []
                data[pair[0]].append(pair[1])
    
        with open(self.output_path, 'w') as outfile:
            json.dump(data, outfile)
