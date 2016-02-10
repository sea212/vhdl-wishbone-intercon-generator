#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# standard
import os
import sys
import configparser
# custom
from wb_component import *
from wb_intercon import *

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
        self.__intercon = WishboneIntercon()
        
    #def __del__(self):
        ''' clean up '''
    #    self.__config

    def parse(self, file_to_parse="./cfg/wishbone.ini"):
        ''' parse the given wishbone config file '''
        self.__config.read(file_to_parse)

        # sections: general, master, <prefix>slave<sufix>
        for section in self.__config.sections():
            secl = section.lower()

            for key in self.__config[section]:
                keyl = key.lower()

                # parse general intercon configuration
                if "general" in secl:
                    if keyl == "tga_bits":
                        self.__intercon.setTgaBits(int(self.__config[section][key]))
                    elif keyl == "tgc_bits":
                        self.__intercon.setTgcBits(int(self.__config[section][key]))
                    elif keyl == "tgd_bits":
                        self.__intercon.setTgdBits(int(self.__config[section][key]))
                    elif keyl == "data_bus_size":
                        self.__intercon.setDataBusWidth(int(self.__config[section][key]))
                    elif keyl == "address_bus_width":
                        self.__intercon.setAdressBusWidth(int(self.__config[section][key]))
                    else:
                        raise configparser.Error("unknown key: "+key)
                elif "master" in secl or "slave" in secl:
                    # TODO: create master,slave and them to intercon
                    # TODO: fix super call for WishboneComponent.__str__
                    # in WishboneMaster and WishboneSlave
                    wbmaster = WishboneMaster(WishboneComponent)
                    self.__intercon.setMaster(wbmaster)
                    
                    if "slave" in secl:
                        pass
                else:
                    raise configparser.Error("unknown section: "+section)

    def printConfigContent(self):
        ''' print parsed information nicely to console '''
        print(self.__intercon)
        
    
    def generateIntercon(file_to_create="./vhdl/wb_intercon.vhdl"):
        ''' generate Intercon '''
