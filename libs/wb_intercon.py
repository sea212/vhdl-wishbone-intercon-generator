#! /usr/bin/env python
# -*- coding: UTF-8 -*-

# standard
import os
import sys
# custom
from wb_component import *

''' this programm offers functions to read wishbone config iles
and generate an intercon in vhdl '''

__author__ = "Harald Heckmann"
__copyright__ = "Copyright 2016"
__credits__ = ["Prof. Dr. Steffen Reith", "Harald Heckmann"]
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Harald Heckmann"
__email__ = "harald.heckmann@student.hs-rm.de"
__status__ = "Development (alpha)"

class WishboneIntercon:
    ''' WishboneIntercon is a class which is used to gather all informations,
which are required to create an intercon, such as general information,
in this state of development one master object and slave objects '''

    def __init__(self):
        ''' initialize the class by initializing all fields '''
        self._name = "wb_intercon"
        self._tgabits = None
        self._tgcbits = None
        self._tgdbits = None
        self._databuswidth = None
        self._addressbuswidth = None
        self._master = None
        self._slaves = set()

    def __str__(self):
        strrepr = "------------------ Intercon ------------------"\
                + "\nName : "+str(self._name)\
                + "\nAmount of TGA bits: "+str(self._tgabits)\
                + "\nAmount of TGC bits: "+str(self._tgcbits)\
                + "\nAmount of TGD bits: "+str(self._tgdbits)\
                + "\nSize of Databus: "+str(self._databuswidth)\
                + "\nSize of Addressbus: "+str(self._addressbuswidth)

        if self._master != None:
            strrepr += "\n"+str(self._master)

        for slave in self._slaves:
            strrepr += "\n"+str(slave)

        return strrepr.replace("None", "Not defined")

    def setName(self, name):
        ''' set a name for the intercon
            @param name: name to set
            @type name: String
            @raise TypeError: raised if parameter type mismatch is found
            @rtype: Boolean
            @return: true on success, false otherwise
        '''
        try:
            if not isinstance(name, str):
                raise TypeError("name got wrong type,"
                    +"excepted: String, got: "+str(type(name)))
        except TypeError as e:
            print("WishboneComponent.setName:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self._name = name
        return True

    def getName(self):
        ''' get the name of the intercon
            @raise UnboundLocalError: raised if no name was set yet
            @rtype: String
            @return: name on success, None otherwise
        '''
        try:
            if self._name == None:
                raise UnboundLocalError("Name was not set yet")
        except UnboundLocalError as e:
            print("WishboneComponent.getName:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self._name

    def setTgaBits(self, tgabits):
        ''' Set amount of tgabits, which can be transfered in intercon
            @param tgabits: number of tga bits (=tga bus width in intercon)
            @type tgabits: unsigned int
            @raise TypeError: raised if parameter type mismatch is found
            @raise ValueError: raised if a variables value is out of range
            @rtype: boolean
            @return: true on success, false otherwise
        '''
        try:
            if isinstance(tgabits, int):
                if tgabits < 0:
                    raise ValueError("tgabits is negative")
            else:
                raise TypeError("tgabits got wrong type,"
                    +"excepted: (unsigned) int, got: "+str(type(tgabits)))
        except TypeError as e:
            print("WishboneIntercon.setTgaBits:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneIntercon.setTgaBits:\n"
                +"\tValueError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self._tgabits = tgabits

        return True
        
    def getTgaBits(self):
        ''' get amount of tga bits in intercon
            @raise UnboundLocalError: raised if tgabits has not been set yet
            @rtype: Integer
            @return: amount of tgabits in intercon on success, None otherwise
        '''
        try:
            if self._tgabits == None:
                raise UnboundLocalError("amount of tga bits has not been set yet")
        except UnboundLocalError as e:
            print("WishboneComponent.getTgaBits:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self._tgabits

    def setTgcBits(self, tgcbits):
        ''' Set amount of tgcbits, which can be transfered in intercon
            @param tgcbits: number of tgc bits (=tgc bus width in intercon)
            @type tgcbits: unsigned int
            @raise TypeError: raised if parameter type mismatch is found
            @raise ValueError: raised if a variables value is out of range
            @rtype: boolean
            @return: true on success, false otherwise
        '''
        try:
            if isinstance(tgcbits, int):
                if tgcbits < 0:
                    raise ValueError("tgcbits is negative")
            else:
                raise TypeError("tgcbits got wrong type,"
                    +"excepted: (unsigned) int, got: "+str(type(tgcbits)))
        except TypeError as e:
            print("WishboneIntercon.getTgcBits:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneIntercon.getTgcBits:\n"
                +"\tValueError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self._tgcbits = tgcbits

        return True
        

    def getTgcBits(self):
        ''' get amount of tgc bits in intercon
            @raise UnboundLocalError: raised if no width for addressbus was set yet
            @rtype: Integer
            @return: amount of tgcbits in intercon on success, None otherwise
        '''
        try:
            if self._tgcbits == None:
                raise UnboundLocalError("amount of tgc bits has not been set yet")
        except UnboundLocalError as e:
            print("WishboneComponent.getTgcBits:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self._tgcbits


    def setTgdBits(self, tgdbits):
        ''' Set amount of tgdbits, which can be transfered in intercon
            @param tgdbits: number of tgd bits (=tgd bus width in intercon)
            @type tgdbits: unsigned int
            @raise TypeError: raised if parameter type mismatch is found
            @raise ValueError: raised if a variables value is out of range
            @rtype: boolean
            @return: true on success, false otherwise
        '''
        try:
            if isinstance(tgdbits, int):
                if tgdbits < 0:
                    raise ValueError("tgdbits is negative")
            else:
                raise TypeError("tgdbits got wrong type,"
                    +"excepted: (unsigned) int, got: "+str(type(tgdbits)))
        except TypeError as e:
            print("WishboneIntercon.getTgdBits:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneIntercon.getTgdBits:\n"
                +"\tValueError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self._tgdbits = tgdbits

        return True
        

    def getTgdBits(self):
        ''' get amount of tgd bits in intercon
            @raise UnboundLocalError: raised if no width for addressbus was set yet
            @rtype: Integer
            @return: amount of tgdbits in intercon on success, None otherwise
        '''
        try:
            if self._tgdbits == None:
                raise UnboundLocalError("amount of tgd bits has not been set yet")
        except UnboundLocalError as e:
            print("WishboneComponent.getTgdBits:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self._tgdbits


    def setAdressBusWidth(self, width):
        ''' Set the width of the addressbus of the intercon
            @param width: bus width in bits (decimal)
            @type width: Integer
            @raise TypeError: raised if parameter type mismatch is found
            @raise ValueError: raised if width is negative
            @rtype: boolean
            @return: true on success, false otherwise
        '''
        try:
            if not isinstance(width, int):
                raise TypeError("width got the wront type,"
                    +"excepted: Integer, got: "+str(type(width)))
            else:
                if width < 0:
                    raise ValueError("Buswidth cannot be negative")
        except TypeError as e:
            print("WishboneIntercon.setAdressBusWidth:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneIntercon.setAdressBusWidth:\n"
                +"\tValueError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self._addressbuswidth = width
        return True

    def getAdressBusWidth(self):
        ''' get the width of the addressbus
            @raise UnboundLocalError: raised if no width for addressbus was set yet
            @rtype: Integer
            @return: width of addressbus on success, None otherwise
        '''
        try:
            if self._addressbuswidth == None:
                raise UnboundLocalError("width of addressbus was not set yet")
        except UnboundLocalError as e:
            print("WishboneIntercon.getAdressBusWidth:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self._addressbuswidth


    def setDataBusWidth(self, width):
        ''' Set the width of the databus of the wishbone intercon
            @param width: bus width in bits (decimal)
            @type width: Integer
            @raise TypeError: raised if parameter type mismatch is found
            @raise ValueError: raised if width is negative
            @rtype: boolean
            @return: true on success, false otherwise
        '''
        try:
            if not isinstance(width, int):
                raise TypeError("width got the wront type,"
                    +"excepted: Integer, got: "+str(type(width)))
            else:
                if width < 0:
                    raise ValueError("Buswidth cannot be negative")
        except TypeError as e:
            print("WishboneIntercon.setDataBusWidth:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneIntercon.setDataBusWidth:\n"
                +"\tValueError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self._databuswidth = width
        return True

    def getDataBusWidth(self):
        ''' get the width of the databus
            @raise UnboundLocalError: raised if no width for databus was set yet
            @rtype: Integer
            @return: width of databus on success, None otherwise
        '''
        try:
            if self._databuswidth == None:
                raise UnboundLocalError("width of databus was not set yet")
        except UnboundLocalError as e:
            print("WishboneIntercon.getDataBusWidth:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self._databuswidth

    def setMaster(self, wbmaster):
        ''' set the only wishbone master component of intercon
            @param wbmaster: WishboneMaster Object containing informations for 
                             a master module
            @type wbmaster: WishboneMaster (superclass: WishboneComponent)
            @raise TypeError: raised if parameter type mismatch is found
            @rtype: boolean
            @return: true on success, false otherwise
        '''
        try:
            if not isinstance(wbmaster, WishboneMaster):
                raise TypeError("wbmaster got wrong type,"
                    +"excepted: WishboneMaster, got: "+str(type(wbmaster)))
        except TypeError as e:
            print("WishboneIntercon.addMaster:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self._master = wbmaster
        return True

    def getMaster(self):
        ''' get the only wishbone master component for this intercon
            @raise UnboundLocalError: raised if no master was set yet
            @rtype: WishboneMaster
            @return: master component on success, empty master component on fail
        '''

        try:
            if self._master == None:
                raise UnboundLocalError("no master component was set yet")
        except UnboundLocalError as e:
            print("WishboneIntercon.getMaster:\n"
                +"UnboundLocalError occurred: "+e.args[0]+"\nstopping execution")
            return WishboneMaster()

        return self._master

    def addSlave(self, wbslave):
        ''' add a wishbone slave component to intercon
            @param wbslave: WishboneSlave Object containing informations for 
                            a slave module
            @type wbslave: WishboneSlave (superclass: WishboneComponent)
            @raise TypeError: raised if parameter type mismatch is found
            @rtype: boolean
            @return: true on success, false otherwise
        '''
        try:
            if not isinstance(wbslave, WishboneSlave):
                raise TypeError("wbslave got wrong type,"
                    +"excepted: WishboneSlave, got: "+str(type(wbslave)))
        except TypeError as e:
            print("WishboneIntercon.addSlave:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self._slaves.add(wbslave)
        return True

    def getSlaves(self):
        ''' get a list containing all wishbone slaves which have been applied 
            to this intercon object
            @rtype: Set (can be empty) containing WishboneSlave objects
            @return: Set containing all slaves for this intercon
        '''

        return self._slaves
            
