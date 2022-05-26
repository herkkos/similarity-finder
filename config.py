# -*- coding: utf-8 -*-
"""
"""

from os import path
import json

class ConfigManager:
    
    __config_file = "config.json"
    __threshold = 0
    __filetypes = []
    __input_paths = ""
    __input_paths = ""
    __output_path = ""
    
    def __init__(self, file="config.json"):
        if file:
            self.__config_file = file
        
        self.read_from_file()
    
    def __del__(self):
        self.write_to_file()
    
    def read_from_file(self):
        if path.exists(self.__config_file):
            with open(self.__config_file, "r", encoding="utf-8") as read_file:
                data = json.load(read_file)["config"]

            self.__threshold = data["threshold"]
            self.__filetypes = data["filetypes"]
            self.__input_paths = data["inputpaths"]
            self.__output_path = data["outputpath"]
    
    def write_to_file(self):
        data = {}
        data["threshold"] = self.__threshold
        data["filetypes"] = self.__filetypes
        data["inputpaths"] = self.__input_paths
        data["outputpath"] = self.__output_path
    
    def get_config_file(self):
        return self.__config_file
    
    def set_config_file(self, value):
        self.__config_file = value
    
    def get_threshold(self):
        return self.__threshold
    
    def set_threshold(self, value):
        self.__threshold = value
    
    def get_filetypes(self):
        return self.__filetypes
    
    def set_filetypes(self, value):
        self.__filetypes = value
    
    def get_input_paths(self):
        return self.__input_paths
    
    def set_input_paths(self, value):
        self.__input_paths = value
    
    def get_output_path(self):
        return self.__output_path
    
    def set_output_path(self, value):
        self.__output_path = value


