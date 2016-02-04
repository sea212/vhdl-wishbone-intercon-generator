#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import configparser

''' this programm offers functions to read wishbone config files
and generate an intercon in vhdl '''

__author__ = "Harald Heckmann"
__copyright__ = "Copyright 2016"
__credits__ = ["Prof. Dr. Steffen Reith", "Harald Heckmann"]
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Harald Heckmann"
__email__ = "harald.heckmann@student.hs-rm.de"
__status__ = "Development (alpha)"

class WishboneFileManager:
    ''' WishboneFileManager is a class offering functions to properly parse
a wishbone intercon config file '''

    def __init__(self):
        ''' initialize all variables required '''
        self.__config = configparser.ConfigParser()
        
    #def __del__(self):
        ''' clean up '''
    #    self.__config

    def parse(self, file_to_parse="./cfg/wishbone.ini"):
        ''' parse the given wishbone config file '''
        self.__config.read(file_to_parse)

    def printConfigContent(self):
        ''' print parsed information nicely to console '''
        for section in self.__config.sections():
            if "general" in section.lower():
                print("---------- General configuration ----------")

            if "master" in section.lower():
                print("---------- Master: "+self.__config[section]["name"]
                    +" ----------")

            if "slave" in section.lower():
                print("---------- Slave: "+self.__config[section]["name"]
                    +" ----------")

            for key in filter(lambda temp: temp.lower() != "name", self.__config[section]):
                print("\t"+key+": "+self.__config[section][key])
    
    def generateIntercon(file_to_create="./vhdl/wb_intercon.vhdl"):
        ''' generate Intercon '''
