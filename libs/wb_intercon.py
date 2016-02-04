#not /usr/bin/env python
# -*- coding: UTF-8 -*-

import configparser

# add custom libraries
path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'libs'))
if not path in sys.path:
    print(path)
    sys.path.insert(1, path)
del path

from wb_file_manager import WishboneMaster,WishboneSlave

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
        self.__tgabits = None
        self.__tgcbits = None
        self.__tgdbits = None
        self.__databuswidth = None
        self.__addressbuswidth = None
        self.__master = None
        self.__slaves = set()

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
                    +"excepted: (unsigned) int, got: "+type(tgabits))
        except TypeError as e:
            print("WishboneIntercon.setTgaBits:\n"
                +"\tTypeError occurred: "+e.value+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneIntercon.setTgaBits:\n"
                +"\tValueError occurred: "+e.value+"\nstopping execution")
            return False

        self.__tgabits = tgabits

        return True
        
    def getTgaBits(self):
        ''' get amount of tga bits in intercon
            @raise UnboundLocalError: raised if tgabits has not been set yet
            @rtype: Integer
            @return: amount of tgabits in intercon on success, None otherwise
        '''
        try:
            if self.__tgabits == None:
                raise UnboundLocalError("amount of tga bits has not been set yet")
        except UnboundLocalError as e:
            print("WishboneComponent.getTgaBits:\n"
                +"\tUnboundLocalError occurred: "+e.value+"\nstopping execution")

        return self.__tgabits

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
                    +"excepted: (unsigned) int, got: "+type(tgcbits))
        except TypeError as e:
            print("WishboneIntercon.getTgcBits:\n"
                +"\tTypeError occurred: "+e.value+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneIntercon.getTgcBits:\n"
                +"\tValueError occurred: "+e.value+"\nstopping execution")
            return False

        self.__tgcbits = tgcbits

        return True
        

    def getTgcBits(self):
        ''' get amount of tgc bits in intercon
            @raise UnboundLocalError: raised if no width for addressbus was set yet
            @rtype: Integer
            @return: amount of tgcbits in intercon on success, None otherwise
        '''
        try:
            if self.__tgcbits == None:
                raise UnboundLocalError("amount of tgc bits has not been set yet")
        except UnboundLocalError as e:
            print("WishboneComponent.getTgcBits:\n"
                +"\tUnboundLocalError occurred: "+e.value+"\nstopping execution")

        return self.__tgcbits


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
                    +"excepted: (unsigned) int, got: "+type(tgdbits))
        except TypeError as e:
            print("WishboneIntercon.getTgdBits:\n"
                +"\tTypeError occurred: "+e.value+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneIntercon.getTgdBits:\n"
                +"\tValueError occurred: "+e.value+"\nstopping execution")
            return False

        self.__tgdbits = tgdbits

        return True
        

    def getTgdBits(self):
        ''' get amount of tgd bits in intercon
            @raise UnboundLocalError: raised if no width for addressbus was set yet
            @rtype: Integer
            @return: amount of tgdbits in intercon on success, None otherwise
        '''
        try:
            if self.__tgdbits == None:
                raise UnboundLocalError("amount of tgd bits has not been set yet")
        except UnboundLocalError as e:
            print("WishboneComponent.getTgdBits:\n"
                +"\tUnboundLocalError occurred: "+e.value+"\nstopping execution")

        return self.__tgdbits


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
                    +"excepted: Integer, got: "+type(width))
            else:
                if width < 0:
                    raise ValueError("Buswidth cannot be negative")
        except TypeError as e:
            print("WishboneIntercon.setAdressBusWidth:\n"
                +"\tTypeError occurred: "+e.value+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneIntercon.setAdressBusWidth:\n"
                +"\tValueError occurred: "+e.value+"\nstopping execution")
            return False

        self.__addressbuswidth = width
        return True

    def getAdressBusWidth(self):
        ''' get the width of the addressbus
            @raise UnboundLocalError: raised if no width for addressbus was set yet
            @rtype: Integer
            @return: width of addressbus on success, None otherwise
        '''
        try:
            if self.__addressbuswidth == None:
                raise UnboundLocalError("width of addressbus was not set yet")
        except UnboundLocalError as e:
            print("WishboneIntercon.getAdressBusWidth:\n"
                +"\tUnboundLocalError occurred: "+e.value+"\nstopping execution")

        return self.__addressbuswidth


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
                    +"excepted: Integer, got: "+type(width))
            else:
                if width < 0:
                    raise ValueError("Buswidth cannot be negative")
        except TypeError as e:
            print("WishboneIntercon.setDataBusWidth:\n"
                +"\tTypeError occurred: "+e.value+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneIntercon.setDataBusWidth:\n"
                +"\tValueError occurred: "+e.value+"\nstopping execution")
            return False

        self.__databuswidth = width
        return True

    def getDataBusWidth(self):
        ''' get the width of the databus
            @raise UnboundLocalError: raised if no width for databus was set yet
            @rtype: Integer
            @return: width of databus on success, None otherwise
        '''
        try:
            if self.__databuswidth == None:
                raise UnboundLocalError("width of databus was not set yet")
        except UnboundLocalError as e:
            print("WishboneIntercon.getDataBusWidth:\n"
                +"\tUnboundLocalError occurred: "+e.value+"\nstopping execution")

        return self.__databuswidth

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
                    +"excepted: WishboneMaster, got: "+type(wbmaster))
        except TypeError as e:
            print("WishboneIntercon.addMaster:\n"
                +"\tTypeError occurred: "+e.value+"\nstopping execution")
            return False

        self.__master = wbmaster
        return True

    def getMaster(self):
        ''' get the only wishbone master component for this intercon
            @raise UnboundLocalError: raised if no master was set yet
            @rtype: WishboneMaster
            @return: master component on success, empty master component on fail
        '''

        try:
            if self.__master == None:
                raise UnboundLocalError("no master component was set yet")
        except UnboundLocalError as e:
            print("WishboneIntercon.getMaster:\n"
                +"UnboundLocalError occurred: "+e.value+"\nstopping execution")
            return WishboneMaster()

        return self.__master

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
                    +"excepted: WishboneSlave, got: "+type(wbslave))
        except TypeError as e:
            print("WishboneIntercon.addSlave:\n"
                +"\tTypeError occurred: "+e.value+"\nstopping execution")
            return False

        self.__slaves.add(wbslave)
        return True

    def getSlaves(self):
        ''' get a list containing all wishbone slaves which have been applied 
            to this intercon object
            @rtype: Set (can be empty) containing WishboneSlave objects
            @return: Set containing all slaves for this intercon
        '''

        return self.__slaves
            
