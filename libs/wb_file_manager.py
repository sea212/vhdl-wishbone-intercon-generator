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
        wasfound = False

        # sections: general, master, <prefix>slave<sufix>
        for section in self.__config.sections():
            secl = section.lower()

            if "master" in secl:
                wbcomp = WishboneMaster()
            elif "slave" in secl:
                wbcomp = WishboneSlave()

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
                    elif keyl == "data_bus_width":
                        self.__intercon.setDataBusWidth(int(self.__config[section][key]))
                    elif keyl == "address_bus_width":
                        self.__intercon.setAdressBusWidth(int(self.__config[section][key]))
                    else:
                        raise configparser.Error("unknown key: "+key)

                # parse configurations both, master and slave, have
                elif "master" in secl or "slave" in secl:
                    wasfound = True
                    # parse confiurations only the master has
                    if "master" in secl:
                        if keyl == "address_bus_width":
                            wbcomp.setAddressBusWidth(int(self.__config[section][key]))
                        else:
                            wasfound = False

                    # parse configurations only the slave has
                    if "slave" in secl:
                        if keyl == "base_address":
                            wbcomp.setBaseAddress(int(self.__config[section][key], 16))
                        elif keyl == "address_size":
                            wbcomp.setAddressSize(int(self.__config[section][key], 16))
                        elif keyl == "addressing_granularity":
                            if self.__config[section][key].lower() == "byte":
                                wbcomp.setAddressingGranularity(wbcomp.CONST.BYTE)
                            elif self.__config[section][key].lower() == "word":
                                wbcomp.setAddressingGranularity(wbcomp.CONST.WORD)
                            else:
                                raise ValueError("Adressinggranularity can be\
                                    byte or word, got: "+self.__config[section][key])
                        elif keyl == "word_size":
                            wbcomp.setWordSize(int(self.__config[section][key]))
                        elif keyl == "address_bus_high":
                            wbcomp.setHighestAddressBit(int(self.__config[section][key]))
                        elif keyl == "address_bus_low":
                            wbcomp.setLowestAddressBit(int(self.__config[section][key]))
                        else:
                            wasfound = False

                    if not wasfound:
                        if keyl == "name":
                            wbcomp.setName(str(self.__config[section][key]))
                        elif keyl == "data_bus_width":
                            wbcomp.setDataBusWidth(int(self.__config[section][key]))
                        elif keyl == "endianess":
                            if self.__config[section][key].lower() == "big":
                                wbcomp.setEndianess(wbcomp.CONST.BENDIAN)
                            elif self.__config[section][key].lower() == "little":
                                wbcomp.setEndianess(wbcomp.CONST.LENDIAN)
                            else:
                                raise ValueError("Endianess can be big/little,\
                                                got: "+self.__config[section][key])
                        elif keyl == "data_flow":
                            if self.__config[section][key].lower() == "r":
                                wbcomp.setDataFlow(wbcomp.CONST.READ)
                            elif self.__config[section][key].lower() == "w":
                                wbcomp.setDataFlow(wbcomp.CONST.WRITE)
                            elif self.__config[section][key].lower() == "rw":
                                wbcomp.setDataFlow(wbcomp.CONST.RW)
                            else:
                                raise ValueError("Dataflow can be: r,w or rw,\
                                                got: "+self.__config[section][key])
                        elif keyl == "err":
                            if self.__config[section][key].lower() == "true":
                                wbcomp.setErrorSignal(True)
                            elif self.__config[section][key].lower() == "false":
                                wbcomp.setErrorSignal(False)
                            else:
                                raise ValueError("err can be: true or false,\
                                    got: "+self.__config[section][key])

                        elif keyl == "rty":
                            if self.__config[section][key].lower() == "true":
                                wbcomp.setRetrySignal(True)
                            elif self.__config[section][key].lower() == "false":
                                wbcomp.setRetrySignal(False)
                            else:
                                raise ValueError("rty can be: true or false,\
                                    got: "+self.__config[section][key])
                        elif keyl == "tga":
                            if self.__config[section][key].lower() == "true":
                                wbcomp.setTgaSignal(True)
                            elif self.__config[section][key].lower() == "false":
                                wbcomp.setTgaSignal(False)
                            else:
                                raise ValueError("tga can be: true or false,\
                                    got: "+self.__config[section][key])
                        elif keyl == "tgc":
                            if self.__config[section][key].lower() == "true":
                                wbcomp.setTgcSignal(True)
                            elif self.__config[section][key].lower() == "false":
                                wbcomp.setTgcSignal(False)
                            else:
                                raise ValueError("tgc can be: true or false,\
                                    got: "+self.__config[section][key])
                        elif keyl == "tgd":
                            if self.__config[section][key].lower() == "true":
                                wbcomp.setTgdSignal(True)
                            elif self.__config[section][key].lower() == "false":
                                wbcomp.setTgdSignal(False)
                            else:
                                raise ValueError("tgd can be: true or false,\
                                    got: "+self.__config[section][key])
                        else:
                            raise configparser.Error("unknown key: "+key)

                    if "master" in secl: self.__intercon.setMaster(wbcomp)
                    elif "slave" in secl: self.__intercon.addSlave(wbcomp)
                else:
                    raise configparser.Error("unknown section: "+section)

    def printConfigContent(self):
        ''' print parsed information nicely to console '''
        print(self.__intercon)
        
    
    def generateIntercon(file_to_create="./vhdl/wb_intercon.vhdl"):
        ''' generate Intercon '''
