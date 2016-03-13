#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# standard
import os
#import sys
import configparser
from datetime import datetime
from copy import copy
# custom
from wb_component import *
from wb_intercon import *

''' this programm offers functions to read wishbone config files
and generate an intercon in vhdl '''

__author__ = "Harald Heckmann"
__copyright__ = "Copyright 2016"
__credits__ = ["Prof. Dr. Steffen Reith (steffen.reith@hs-rm.de)", \
                "Harald Heckmann (harald.heckmann@student.hs-rm.de)"]
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Harald Heckmann"
__email__ = "harald.heckmann@student.hs-rm.de"
__status__ = "Development (beta)"

class WishboneFileManager:
    ''' WishboneFileManager is a class offering functions to properly parse
a wishbone intercon config file '''

    def __init__(self):
        ''' initialize all variables required '''
        self.__config = configparser.ConfigParser()
        self.__intercon = WishboneIntercon()

        self._workdir = os.getcwd()+"/"
        self._tmplinter = self._workdir+"vhdl/template_intercon.tmpl"
        self._vhdlinter = self._workdir+"vhdl/wb_intercon.vhdl"
        self._tmplslave = self._workdir+"vhdl/template_slave.tmpl"

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
            elif "general" in secl: 
                pass
            else:
                raise configparser.Error("unknown section: "+section)

            for key in self.__config[section]:
                keyl = key.lower()

                # parse general intercon configuration
                if "general" in secl:
                    if keyl == "name":
                        self.__intercon.setName(str(self.__config[section][key]))
                        self._vhdlinter = self._workdir+"vhdl/"+self.__intercon.getName()+".vhdl"
                    elif keyl == "tga_bits":
                        self.__intercon.setTgaBits(int(self.__config[section][key]))
                    elif keyl == "tgc_bits":
                        self.__intercon.setTgcBits(int(self.__config[section][key]))
                    elif keyl == "tgd_bits":
                        self.__intercon.setTgdBits(int(self.__config[section][key]))
                    elif keyl == "data_bus_width":
                        self.__intercon.setDataBusWidth(int(self.__config[section][key]))
                    elif keyl == "address_bus_width":
                        self.__intercon.setAddressBusWidth(int(self.__config[section][key]))
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

    def printConfigContent(self):
        ''' print parsed information nicely to console '''
        print(self.__intercon)

    
    def generateIntercon(self):
        ''' generate intercon and write it to a vhdl file'''
        # read template
        with open(self._tmplinter, "r") as template:
            content = template.read()

        # replace placeholders, header
        content = content.replace("%date%", datetime.now().__str__())
        content = content.replace("%iname%", self.__intercon.getName())
        
        # master
        master = self.__intercon.getMaster()
        content = content.replace("%mname%", master.getName())
        content = content.replace("%mdbwidth%", str(master.getDataBusWidth()-1))
        content = content.replace("%madwidth%", str(master.getAddressBusWidth()-1))
        content = content.replace("%mselwidth%", str((master.getDataBusWidth() >> 3)-1))
        
        # additional port definitions
        additional = ""
        # additional signal definitions
        s_additional = ""
        # additional signal assignments
        a_additional = ""

        # set optional master signals
        if master.getErrorSignal():
            additional += "\n\t\t\t"+master.getName()+"_err_i : out std_logic := '0';"
            s_additional += "\nsignal err : std_logic := '0';"
            a_additional += "\n\t"+master.getName()+"_err_i <= err;"

        if master.getRetrySignal():
            additional += "\n\t\t\t"+master.getName()+"_rty_i : out std_logic := '0';"
            s_additional += "\nsignal rty : std_logic := '0';"
            a_additional += "\n\t"+master.getName()+"_rty_i <= rty;"

        if master.getTgaSignal():
            additional += "\n\t\t\t"+master.getName()+"_tga_o : in  std_logic_vector("\
                +str(self.__intercon.getTgaBits()-1)+" downto 0);"
            s_additional += "\nsignal tga : std_logic_vector(%d downto 0) := (others => '0');" % \
                            (self.__intercon.getTgaBits()-1)
            a_additional += "\n\ttga <= "+master.getName()+"_tga_o;"

        if master.getTgcSignal():
            additional += "\n\t\t\t"+master.getName()+"_tgc_o : in  std_logic_vector("\
                +str(self.__intercon.getTgcBits()-1)+" downto 0);"
            s_additional += "\nsignal tgc : std_logic_vector(%d downto 0) := (others => '0');" % \
                            (self.__intercon.getTgcBits()-1)
            a_additional += "\n\ttgc <= "+master.getName()+"_tgc_o;"

        if master.getTgdSignal():
            additional += "\n\t\t\t"+master.getName()+"_tgd_i : out std_logic_vector("\
                +str(self.__intercon.getTgdBits()-1)+" downto 0) := (others => '0');"
            additional += "\n\t\t\t"+master.getName()+"_tgd_o : in  std_logic_vector("\
                +str(self.__intercon.getTgdBits()-1)+" downto 0);"
            s_additional += "\nsignal tgdm2s : std_logic_vector(%d downto 0) := (others => '0');" % \
                            (self.__intercon.getTgdBits()-1)
            s_additional += "\nsignal tgds2m : std_logic_vector(%d downto 0) := (others => '0');" % \
                            (self.__intercon.getTgdBits()-1)
            a_additional += "\n\ttgdm2s <= "+master.getName()+"_tgd_o;"
            a_additional += "\n\t"+master.getName()+"_tgd_i <= tgds2m;"

        content = content.replace("%madditional%", additional)
        content = content.replace("%additonalsignals%", s_additional)
        content = content.replace("%additional_assignments%", a_additional)

        # slave
        with open(self._tmplslave, "r") as template:
            fb_scontent = template.read()

        slavedefinitions = ""

        slavenr = 0;
        slavemax = len(self.__intercon.getSlaves())

        # address decoder and interconnection
        interconnection = ""
        # prevent latches when cyc is low (no valid cycle)
        antilatch = "\n\t\t\t\t\t\t-- prevent latches on invalid slave selection"

        for slave in sorted(self.__intercon.getSlaves()):
            scontent = copy(fb_scontent)
            scontent = scontent.replace("%sname%", slave.getName())
            scontent = scontent.replace("%sdbwidth%", str(slave.getDataBusWidth()-1))
            scontent = scontent.replace("%sadhi%", str(slave.getHighestAddressBit()))
            scontent = scontent.replace("%sadlo%", str(slave.getLowestAddressBit()))
            scontent = scontent.replace("%sselwidth%", str((slave.getDataBusWidth() >> 3)-1))

            additional = ""

            # define address decoder and interconnection
            if slavenr == 0:
                interconnection += "\n\t\t\t\t\t-- Baseaddress: "+hex(slave.getBaseAddress())\
                                + ", size: "+hex(slave.getAddressSize())
                interconnection += "\n\t\t\t\t\tif (to_integer(unsigned(adr)) <= "\
                        +str((slave.getBaseAddress()+slave.getAddressSize()))+") then"
            else:
                interconnection += "\n\t\t\t\t\t-- Baseaddress: "+hex(slave.getBaseAddress())\
                        + ", size: "+hex(slave.getAddressSize())
                interconnection += "\n\t\t\t\t\telsif (to_integer(unsigned(adr)) <= "\
                        +str((slave.getBaseAddress()+slave.getAddressSize()))+") then"

            slavenr += 1

            antilatch += "\n\t\t\t\t\t\t"+slave.getName()+"_dat_i <= (others => '0');"
            antilatch += "\n\t\t\t\t\t\t"+slave.getName()+"_sel_i <= (others => '0');"

            # endianess conversion
            if slave.getEndianess() == master.getEndianess():
                interconnection += "\n\t\t\t\t\t\t"+slave.getName()+"_dat_i <= datm2s;"
                interconnection += "\n\t\t\t\t\t\tdats2m <= "+slave.getName()+"_dat_o;"
                interconnection += "\n\t\t\t\t\t\t"+slave.getName()+"_sel_i <= sel;"
            else:
                interconnection += "\n\t\t\t\t\t\t-- conversion of endianess"
                mbw = master.getDataBusWidth()-1
                sbw = slave.getDataBusWidth()-1
                selmax = (master.getDataBusWidth() >> 3)

                for i in range(0, (slave.getDataBusWidth() >> 3)):
                    datm2shi = str(mbw-8*i)
                    if i != (slave.getDataBusWidth() >> 3): datm2slo = str(mbw-8*(i+1)+1)
                    else: datm2slo = "0"

                    dats2mhi = str(sbw-8*i)
                    if i != (slave.getDataBusWidth() >> 3): dats2mlo = str(sbw-8*(i+1)+1)
                    else: dats2mlo = "0"

                    phi = str(8*(i+1)-1) 
                    if i != 0: plo = str(8*i)
                    else: plo = "0"

                    interconnection += "\n\t\t\t\t\t\t"+slave.getName()+"_sel_i("\
                        +str(i)+" downto "+str(i)+") <= sel("+str(selmax-(i+1))+" downto "\
                        +str(selmax-(i+1))+");"
                    interconnection += "\n\t\t\t\t\t\t"+slave.getName()+"_dat_i("\
                        +phi+" downto "+plo+") <= datm2s("+datm2shi+" downto "\
                        +datm2slo+");"
                    interconnection += "\n\t\t\t\t\t\tdats2m("+datm2shi+" downto "\
                        +datm2slo+") <= "+slave.getName()+"_dat_o("+phi+" downto "\
                        +plo+");"

                interconnection += "\n\t\t\t\t\t\t-- end of conversion"

            interconnection += "\n\t\t\t\t\t\tack <= "+slave.getName()+"_ack_o;"
            interconnection += "\n\t\t\t\t\t\t"+slave.getName()+"_adr_i <= adr("\
                            +str(slave.getHighestAddressBit())+" downto "\
                            +str(slave.getLowestAddressBit())+");"
            interconnection += "\n\t\t\t\t\t\t"+slave.getName()+"_cyc_i <= cyc;"
            interconnection += "\n\t\t\t\t\t\t"+slave.getName()+"_stb_i <= stb;"
            interconnection += "\n\t\t\t\t\t\t"+slave.getName()+"_we_i <= we;"

            antilatch += "\n\t\t\t\t\t\t"+slave.getName()+"_adr_i <= (others => '0');"
            antilatch += "\n\t\t\t\t\t\t"+slave.getName()+"_cyc_i <= '0';"
            antilatch += "\n\t\t\t\t\t\t"+slave.getName()+"_stb_i <= '0';"
            antilatch += "\n\t\t\t\t\t\t"+slave.getName()+"_we_i <= '0';"

            # set optional slave signals
            if slave.getErrorSignal():
                additional += ";\n\t\t\t"+slave.getName()+"_err_o : in  std_logic"
                interconnection += "\n\t\t\t\t\t\terr <= "+slave.getName()+"_err_o;"

            if slave.getRetrySignal():
                additional += ";\n\t\t\t"+slave.getName()+"_rty_o : in  std_logic"
                interconnection += "\n\t\t\t\t\t\trty <= "+slave.getName()+"_rty_o;"

            if slave.getTgaSignal():
                additional += ";\n\t\t\t"+slave.getName()+"_tga_i : out std_logic_vector("\
                    +str(self.__intercon.getTgaBits()-1)+" downto 0) := (others => '0')"
                interconnection += "\n\t\t\t\t\t\t"+slave.getName()+"_tga_i <= tga;"
                antilatch += "\n\t\t\t\t\t\t"+slave.getName()+"_tga_i <= (others => '0');"

            if slave.getTgcSignal():
                additional += ";\n\t\t\t"+slave.getName()+"_tgc_i : out std_logic_vector("\
                    +str(self.__intercon.getTgcBits()-1)+" downto 0) := (others => '0')"
                interconnection += "\n\t\t\t\t\t\t"+slave.getName()+"_tgc_i <= tgc;"
                antilatch += "\n\t\t\t\t\t\t"+slave.getName()+"_tgc_i <= (others => '0');"

            if slave.getTgdSignal():
                additional += ";\n\t\t\t"+slave.getName()+"_tgd_i : out std_logic_vector("\
                    +str(self.__intercon.getTgdBits()-1)+" downto 0) := (others => '0')"
                additional += ";\n\t\t\t"+slave.getName()+"_tgd_o : in  std_logic_vector("\
                    +str(self.__intercon.getTgdBits()-1)+" downto 0)"
                interconnection += "\n\t\t\t\t\t\t"+slave.getName()+"_tgd_i <= tgdm2s;"
                antilatch += "\n\t\t\t\t\t\t"+slave.getName()+"_tgd_i <= (others => '0');"
                interconnection += "\n\t\t\t\t\t\ttgds2m <= "+slave.getName()+"_tgd_o;"

            if (slavenr != slavemax):
                additional += ";"

            slavedefinitions += scontent.replace("%sadditional%", additional)+"\n"
            

        antilatch += "\n\t\t\t\t\t\tdats2m <= (others => '0');"
        antilatch += "\n\t\t\t\t\t\tack <= '0';"
        antilatch += "\n\t\t\t\t\t\terr <= '0';"
        antilatch += "\n\t\t\t\t\t\trty <= '0';"
        antilatch += "\n\t\t\t\t\t\ttgds2m <= (others => '0');"
        interconnection += "\n\t\t\t\t\telse%antilatch%\n\t\t\t\t\tend if;"

        content = content.replace("%slaves%", slavedefinitions)
        content = content.replace("%interconnection%", interconnection)
        content = content.replace("%antilatch%", antilatch)
        content = content.replace("%antilatch2%", antilatch.replace("\n\t\t\t\t\t\t",\
                 "\n\t\t\t\t\t").replace("slave selection","cycles"))

        # signal definitions
        # required signals
        content = content.replace("%intabwidth%", str(self.__intercon.getAddressBusWidth()-1))
        content = content.replace("%intdbwidth%", str(self.__intercon.getDataBusWidth()-1))
        content = content.replace("%selwidth%", str((self.__intercon.getDataBusWidth() >> 3)-1))

        with open(self._vhdlinter, "w") as intercon:
            intercon.write(content)

        
