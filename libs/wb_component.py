#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# standard
from random import randint

''' this programm offers a class to store abstract informations for wishbone 
master and slave modules, which can be processed afterwards '''

__author__ = "Harald Heckmann"
__copyright__ = "Copyright 2016"
__credits__ = ["Prof. Dr. Steffen Reith", "Harald Heckmann"]
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Harald Heckmann"
__email__ = "harald.heckmann@student.hs-rm.de"
__status__ = "Development (alpha)"

'''
class Const(object):
    @constant
    def LENDIAN():
        return 0x00000001
    @constant
    def BENDIAN():
        return 0x00000002
    @constant
    def READ():
        return 0x00000003
    @constant
    def WRITE():
        return 0x00000004
    @constant
    def RW():
        return 0x00000005
    @constant
    def SINGLE():
        return 0x00000006
    @constant
    def BURST():
        return 0x00000007
    @constant
    def RMW():
        return 0x00000008
'''

# constants are a serious problem in python...
class Const:
    class ConstError(TypeError): pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const(%s)"%name)
        self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise self.ConstError("Can't unbind const(%s)"%name)
        raise NameError(name)


class WishboneComponent:
    ''' WishboneComponent is a class which offers functions to store information 
and read them again, where the stored informations can be used to describe 
properties, which both, master as well as slave components, use'''

    def __init__(self):
        # masters and slaves common signals:
        # name              = string
        # data_bus_size     = decimal value
        # address_bus_width = decimal value
        # endianess         = big/little
        # data_flow         = r/w/rw
        # data_transfer     = single/burst/rmw
        # err               = true/false
        # rty               = true/false
        # tga               = true/false
        # tgc               = true/false
        # tgd               = true/false
        self.CONST = Const()
        self.CONST.LENDIAN = 0x00000001
        self.CONST.BENDIAN = 0x00000002
        self.CONST.READ = 0x00000003
        self.CONST.WRITE = 0x00000004
        self.CONST.RW = 0x00000005
        self.CONST.SINGLE = 0x00000006
        self.CONST.BURST = 0x00000007
        self.CONST.RMW = 0x00000008
        self.CONST.BYTE = 0x00000009
        self.CONST.WORD = 0x00000010
        
        # one underscore = protected visibility
        # two underscores = private visibility
        self._name = "wbcomp"+str(randint(0,1000))
        self._databuswidth = None
        self._endianess = None
        self._dataflow = None
        #self._datatransfer = None
        self._err = None
        self._rty = None
        self._tga = None
        self._tgc = None
        self._tgd = None

    def __str__(self):
        strrepr = "Name: "+str(self._name)+"\nWidth of databus: "+str(self._databuswidth)

        if self._endianess == None:
            strrepr += "\nEndianess: None"
        else:
            if self._endianess == self.CONST.LENDIAN:
                strrepr += "\nEndianess: Little Endian"
            else:
                strrepr += "\nEndianess: Big Endian"

        if self._dataflow == None:
            strrepr += "\nDirection of dataflow: None"
        else:
            # no switch case is available in python (need to trick with mappings...)
            # so we use if,elif,else...
            if self._dataflow == self.CONST.READ:
                strrepr += "\nDirection of dataflow: Read only"
            elif self._dataflow == self.CONST.WRITE:
                strrepr += "\nDirection of dataflow: Write only"
            else:
                strrepr += "\nDirection of dataflow: Read/Write"

        '''
        if self._datatransfer == None:
            strrepr += "\nDatatransfer cycle: None"
        else:
            # no switch case is available in python (need to trick with mappings...)
            # so we use if,elif,else...
            if self._datatransfer == self.CONST.SINGLE:
                strrepr += "\nDatatransfer cycle: Single"
            elif self._datatransfer == self.CONST.BURST:
                strrepr += "\nDatatransfer cycle: Burst"
            else:
                strrepr += "\nDatatransfer cycle: Read, modify, write"
        '''

        strrepr += "\nEnable error signal: "+str(self._err)+"\nEnable retry signal: "\
                    +str(self._rty)+"\nEnable tga signal: "+str(self._tga)\
                    +"\nEnable tgc signal: "+str(self._tgc)+"\nEnable tgd signal: "\
                    +str(self._tgd)

        return strrepr.replace("None", "Not defined")

    def setName(self, name):
        ''' set a name for a wishbone component
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
        ''' get the name of a wishbone component
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

    def setDataBusWidth(self, width):
        ''' Set the width of the databus of a wishbone component
            @param width: bus width in bits (decimal)
            @type width: Integer
            @raise TypeError: raised if parameter type mismatch is found
            @raise ValueError: raised if width is negative
            @rtype: Boolean
            @return: true on success, false otherwise
        '''
        try:
            if not isinstance(width, int):
                raise TypeError("width got the wrong type,"
                    +"excepted: Integer, got: "+str(type(width)))
            else:
                if width < 0:
                    raise ValueError("Buswidth cannot be negative")
        except TypeError as e:
            print("WishboneComponent.setDataBusWidth:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneComponent.setDataBusWidth:\n"
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
            print("WishboneComponent.getDataBusWidth:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self._databuswidth

    def setEndianess(self, endianess):
        ''' Set the endianess
            @param endianess: can be WishboneComponent.CONST.LENDIAN for little
                            endian or WishboneComponent.CONST.BENDIAN for big
                            endian
            @type endianess: Integer
            @raise TypeError: raised if parameter type mismatch is found
            @raise ValueError: raised if value is neither WishboneComponent.
                                CONST.LENDIAN nor WishboneComponent.CONST.BENDIAN
            @rtype: Boolean
            @return: true on success, false otherwise
        '''
        try:
            if not isinstance(endianess, int):
                raise TypeError("endianess got the wrong type,\
                    excepted: CONST.LENDIAN or CONST.BENDIAN,\
                     got: "+str(type(endianess)))
            else:
                if not (endianess == self.CONST.BENDIAN
                or endianess == self.CONST.LENDIAN):
                    raise ValueError("Unknown endianess (use the given constants)")
        except TypeError as e:
            print("WishboneComponent.setEndianess:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneComponent.setEndianess:\n"
                +"\tValueError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self._endianess = endianess
        return True

    def getEndianess(self):
        ''' get the the endianess
            @raise UnboundLocalError: raised if no endianess was set yet
            @rtype: Integer
            @return: endianess (constant) on success, None otherwise
        '''
        try:
            if self._endianess == None:
                raise UnboundLocalError("endianess was not set yet")
        except UnboundLocalError as e:
            print("WishboneComponent.getEndianess:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self._endianess

    def setDataFlow(self, dataflow):
        ''' define if the module can read or write or both
            @param dataflow: can be WishboneComponent.CONST.READ, .WRITE, .RW
            @type dataflow: Integer
            @raise TypeError: raised if parameter type mismatch is found
            @raise ValueError: raised if value is not: WishboneComponent.CONST
                                .READ, .WRITE, .RW
            @rtype: Boolean
            @return: true on success, false otherwise
        '''
        try:
            if not isinstance(dataflow, int):
                raise TypeError("dataflow got the wrong type,"
                    +"excepted: Integer, got: "+str(type(dataflow)))
            else:
                if not (dataflow == self.CONST.READ or dataflow == self.CONST.WRITE
                or dataflow == self.CONST.RW):
                    raise ValueError("Unknown dataflow (use the given constants)")
        except TypeError as e:
            print("WishboneComponent.setDataFlow:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneComponent.setDataFlow:\n"
                +"\tValueError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self._dataflow = dataflow
        return True

    def getDataFlow(self):
        ''' get the endianess
            @raise UnboundLocalError: raised if no dataflow was set yet
            @rtype: Integer
            @return: dataflow (constant) on success, None otherwise
        '''
        try:
            if self._dataflow == None:
                raise UnboundLocalError("dataflow was not set yet")
        except UnboundLocalError as e:
            print("WishboneComponent.getDataFlow:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self._dataflow

    
    #def setDataTransfer(self, datatransfer):
        ''' define how data will be transfered (single, burst, rmw)
            @param datatransfer: can be WishboneComponent.CONST.SINGLE, .BURST, .RMW
            @type datatransfer: Integer
            @raise TypeError: raised if parameter type mismatch is found
            @raise ValueError: raised if value is not: WishboneComponent.CONST
                                .SINGLE, .BURST, .RMW
            @rtype: Boolean
            @return: true on success, false otherwise
        '''
        '''
        try:
            if not isinstance(datatransfer, int):
                raise TypeError("datatransfer got the wrong type,"
                    +"excepted: Integer, got: "+str(type(datatransfer)))
            else:
                if not (datatransfer == self.CONST.SINGLE or datatransfer == self.CONST.BURST
                or datatransfer == self.CONST.RMW):
                    raise ValueError("Unknown datatransfer (use the given constants)")
        except TypeError as e:
            print("WishboneComponent.setDataTransfer:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneComponent.setDataTransfer:\n"
                +"\tValueError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self._datatransfer = datatransfer
        return True
        '''

    #def getDataTransfer(self):
        ''' get the endianess
            @raise UnboundLocalError: raised if no datatransfer was set yet
            @rtype: Integer
            @return: datatransfer (constant) on success, None otherwise
        '''
        '''
        try:
            if self._datatransfer == None:
                raise UnboundLocalError("datatransfer was not set yet")
        except UnboundLocalError as e:
            print("WishboneComponent.getDataTransfer:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self._datatransfer
        '''
        
    def setErrorSignal(self, enabled):
        ''' activate (true) / deactivate (false) the error signal
            @param enabled: Boolean to activate/deactivate the error signal
            @type enabled: Boolean
            @raise TypeError: raised if parameter type mismatch is found
            @rtype: Boolean
            @return: true on success, false otherwise
        '''
        try:
            if not isinstance(enabled, bool):
                raise TypeError("enabled got the wrong type,"
                    +"excepted: Boolean, got: "+str(type(enabled)))
        except TypeError as e:
            print("WishboneComponent.setErrorSignal:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self._err = enabled
        return True

    def getErrorSignal(self):
        ''' get the enabled state of the error signal
            @raise UnboundLocalError: raised if no state was assigned yet
            @rtype: Boolean
            @return: true/false for used/not used on success, None otherwise
        '''
        try:
            if self._err == None:
                raise UnboundLocalError("error signal was not set yet")
        except UnboundLocalError as e:
            print("WishboneComponent.getErrorSignal:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self._err

    def setRetrySignal(self, enabled):
        ''' activate (true) / deactivate (false) the retry signal
            @param enabled: Boolean to activate/deactivate the retry signal
            @type enabled: Boolean
            @raise TypeError: raised if parameter type mismatch is found
            @rtype: Boolean
            @return: true on success, false otherwise
        '''
        try:
            if not isinstance(enabled, bool):
                raise TypeError("enabled got the wrong type,"
                    +"excepted: Boolean, got: "+str(type(enabled)))
        except TypeError as e:
            print("WishboneComponent.setRetrySignal:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self._rty = enabled
        return True

    def getRetrySignal(self):
        ''' get the enabled state of the retry signal
            @raise UnboundLocalError: raised if no state was assigned yet
            @rtype: Boolean
            @return: true/false for used/not used on success, None otherwise
        '''
        try:
            if self._rty == None:
                raise UnboundLocalError("retry signal was not set yet")
        except UnboundLocalError as e:
            print("WishboneComponent.getRetrySignal:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self._rty

    def setTgaSignal(self, enabled):
        ''' activate (true) / deactivate (false) the tga signal
            @param enabled: Boolean to activate/deactivate the tga signal
            @type enabled: Boolean
            @raise TypeError: raised if parameter type mismatch is found
            @rtype: Boolean
            @return: true on success, false otherwise
        '''
        try:
            if not isinstance(enabled, bool):
                raise TypeError("enabled got the wrong type,"
                    +"excepted: Boolean, got: "+str(type(enabled)))
        except TypeError as e:
            print("WishboneComponent.setTgaSignal:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self._tga = enabled
        return True

    def getTgaSignal(self):
        ''' get the enabled state of the tga signal
            @raise UnboundLocalError: raised if no state was assigned yet
            @rtype: Boolean
            @return: true/false for used/not used on success, None otherwise
        '''
        try:
            if self._tga == None:
                raise UnboundLocalError("tga signal was not set yet")
        except UnboundLocalError as e:
            print("WishboneComponent.getTgaSignal:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self._tga

    def setTgcSignal(self, enabled):
        ''' activate (true) / deactivate (false) the tgc signal
            @param enabled: Boolean to activate/deactivate the tgc signal
            @type enabled: Boolean
            @raise TypeError: raised if parameter type mismatch is found
            @rtype: Boolean
            @return: true on success, false otherwise
        '''
        try:
            if not isinstance(enabled, bool):
                raise TypeError("enabled got the wrong type,"
                    +"excepted: Boolean, got: "+str(type(enabled)))
        except TypeError as e:
            print("WishboneComponent.setTgcSignal:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self._tgc = enabled
        return True

    def getTgcSignal(self):
        ''' get the enabled state of the tgc signal
            @raise UnboundLocalError: raised if no state was assigned yet
            @rtype: Boolean
            @return: true/false for used/not used on success, None otherwise
        '''
        try:
            if self._tgc == None:
                raise UnboundLocalError("tgc signal was not set yet")
        except UnboundLocalError as e:
            print("WishboneComponent.getTgcSignal:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self._tgc

    def setTgdSignal(self, enabled):
        ''' activate (true) / deactivate (false) the tgd signal
            @param enabled: Boolean to activate/deactivate the tgd signal
            @type enabled: Boolean
            @raise TypeError: raised if parameter type mismatch is found
            @rtype: Boolean
            @return: true on success, false otherwise
        '''
        try:
            if not isinstance(enabled, bool):
                raise TypeError("enabled got the wrong type,"
                    +"excepted: Boolean, got: "+str(type(enabled)))
        except TypeError as e:
            print("WishboneComponent.setTgdSignal:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self._tgd = enabled
        return True

    def getTgdSignal(self):
        ''' get the enabled state of the tgd signal
            @raise UnboundLocalError: raised if no state was assigned yet
            @rtype: Boolean
            @return: true/false for used/not used on success, None otherwise
        '''
        try:
            if self._tgd == None:
                raise UnboundLocalError("tgd signal was not set yet")
        except UnboundLocalError as e:
            print("WishboneComponent.getTgdSignal:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self._tgd

class WishboneMaster(WishboneComponent):
    ''' WishboneMaster is a subclass of WishboneComponent and was created to 
store informations from a wishbone component which are present in a master
component, but not in a slave'''
    def __init__(self):
        #initfunction
        # call super
        super().__init__()
        # override name
        self._name = "wbm"
        # set address_bus_width
        self.__addressbuswidth = None

    def __str__(self):
        strrepr = "------------------ Wishbone Master: "+str(self._name)\
                  +" ------------------\n"
        strrepr += super().__str__()
        strrepr += "\nMaster specific:\n\tSize of Addressbus: "\
                + str(self.__addressbuswidth)

        return strrepr.replace("None", "Not defined")

    def setAddressBusWidth(self, width):
        ''' Set the width of the addressbus of a wishbone master component
            @param width: bus width in bits (decimal)
            @type width: Integer
            @raise TypeError: raised if parameter type mismatch is found
            @raise ValueError: raised if width is negative
            @rtype: Boolean
            @return: true on success, false otherwise
        '''
        try:
            if not isinstance(width, int):
                raise TypeError("width got the wrong type,"
                    +"excepted: Integer, got: "+str(type(width)))
            else:
                if width < 0:
                    raise ValueError("Buswidth cannot be negative")
        except TypeError as e:
            print("WishboneComponent.setAddressBusWidth:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneComponent.setAddressBusWidth:\n"
                +"\tValueError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self.__addressbuswidth = width
        return True

    def getAddressBusWidth(self):
        ''' get the width of the addressbus
            @raise UnboundLocalError: raised if no width for addressbus was set yet
            @rtype: Integer
            @return: width of addressbus on success, None otherwise
        '''
        try:
            if self.__addressbuswidth == None:
                raise UnboundLocalError("width of addressbus was not set yet")
        except UnboundLocalError as e:
            print("WishboneComponent.getAddressBusWidth:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self.__addressbuswidth

class WishboneSlave(WishboneComponent):
    ''' WishboneMaster is a subclass of WishboneComponent and was created to 
store informations from a wishbone component which are present in a slave
component, but not in a master'''
    def __init__(self):
        #initfunction
        # List of keywords for slave modules and possible values:
        # same as keywords for master (but address_bus_width), plus:
        # base_address              = hexadecimal value
        # address_size              = hexadecimal value
        # addressing_granularity    = byte/word
        # word_size                 = decimal value
        # address_bus_high          = decimal value
        # address_bus_low           = decimal value (lowest bit = 0)
        # call super
        super().__init__()
        # override name
        self._name = "wbs"+str(randint(0,1000))
        # set slave specific variables
        self.__baseaddress = None
        self.__addresssize = None
        self.__addressinggranularity = None
        self.__wordsize = None
        self.__addressbushigh = None
        self.__addressbuslow = None

    def __str__(self):
        strrepr = "------------------ Wishbone Slave: "+str(self._name)\
                  +" ------------------\n"
        strrepr += super().__str__()
        strrepr += "\nSlave specific:"

        if self.__baseaddress == None:
            strrepr += "\n\tBaseaddress: None"
        else:
            strrepr += "\n\tBaseaddress: "+hex(self.__baseaddress)

        if self.__addresssize == None:
            strrepr += "\n\tAddresssize: None"
        else:
            strrepr += "\n\tAddresssize: "+hex(self.__addresssize)

        if self.__addressinggranularity == None:
            strrepr += "\n\tAddressinggranularity: None"
        else:
            if self.__addressinggranularity == self.CONST.BYTE:
                strrepr += "\n\tAddressinggranularity: Byte"
            else:
                strrepr += "\n\tAddressinggranularity: Word"

        strrepr += "\n\tWordsize: "+str(self.__wordsize)+"\n\tHighest addressbit: "\
                +str(self.__addressbushigh)+"\n\tLowest addressbit: "+str(self.__addressbuslow)
                
        return strrepr.replace("None", "Not defined")

    def setBaseAddress(self, baseadr):
        ''' Set the base address of a wishbone slave component
            @param baseadr: Base address for slave
            @type baseadr: Integer
            @raise TypeError: raised if parameter type mismatch is found
            @raise ValueError: raised if baseadr is negative
            @rtype: Boolean
            @return: true on success, false otherwise
        '''
        try:
            if not isinstance(baseadr, int):
                raise TypeError("baseadr got the wrong type,"
                    +"excepted: Integer, got: "+str(type(baseadr)))
            else:
                if baseadr < 0:
                    raise ValueError("Base address cannot be negative")
        except TypeError as e:
            print("WishboneSlave.setBaseAddress:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneSlave.setBaseAddress:\n"
                +"\tValueError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self.__baseaddress = baseadr
        return True

    def getBaseAddress(self):
        ''' get the base address of the slave
            @raise UnboundLocalError: raised if no baseadr was defined yet
            @rtype: Integer
            @return: Base address on success, None otherwise
        '''
        try:
            if self.__baseaddress == None:
                raise UnboundLocalError("Base address was not set yet")
        except UnboundLocalError as e:
            print("WishboneSlave.getBaseAddress:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self.__baseaddress

    def setAddressSize(self, size):
        ''' Set the address size of a wishbone slave component
            @param size: address size for slave
            @type size: Integer
            @raise TypeError: raised if parameter type mismatch is found
            @raise ValueError: raised if size is negative
            @rtype: Boolean
            @return: true on success, false otherwise
        '''
        try:
            if not isinstance(size, int):
                raise TypeError("size got the wrong type,"
                    +"excepted: Integer, got: "+str(type(size)))
            else:
                if size < 0:
                    raise ValueError("address size cannot be negative")
        except TypeError as e:
            print("WishboneSlave.setAddressSize:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneSlave.setAddressSize:\n"
                +"\tValueError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self.__addresssize = size
        return True

    def getAddressSize(self):
        ''' get the address size of the slave
            @raise UnboundLocalError: raised if address size was not defined yet
            @rtype: Integer
            @return: address size on success, None otherwise
        '''
        try:
            if self.__addresssize == None:
                raise UnboundLocalError("Addresssize was not set yet")
        except UnboundLocalError as e:
            print("WishboneSlave.getAddressSize:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self.__addresssize

    def setAddressingGranularity(self, addressinggranularity):
        ''' Set the addressinggranularity
            @param addressinggranularity: can be WishboneComponent.CONST.BYTE
                                        or WishboneComponent.CONST.WORD
            @type addressinggranularity: Integer
            @raise TypeError: raised if parameter type mismatch is found
            @raise ValueError: raised if value is neither WishboneComponent.
                                CONST.BYTE nor WishboneComponent.CONST.WORD
            @rtype: Boolean
            @return: true on success, false otherwise
        '''
        try:
            if not isinstance(addressinggranularity, int):
                raise TypeError("addressinggranularity got the wrong type,"
                    +"excepted: Integer, got: "+str(type(addressinggranularity)))
            else:
                if not (addressinggranularity == self.CONST.BYTE
                or addressinggranularity == self.CONST.WORD):
                    raise ValueError("Unknown addressinggranularity (use the given constants)")
        except TypeError as e:
            print("WishboneSlave.setAddressingGranularity:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneSlave.setAddressingGranularity:\n"
                +"\tValueError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self.__addressinggranularity = addressinggranularity
        return True

    def getAddressingGranularity(self):
        ''' get the the addressinggranularity
            @raise UnboundLocalError: raised if no addressinggranularity was set yet
            @rtype: Integer
            @return: addressinggranularity (constant) on success, None otherwise
        '''
        try:
            if self.__addressinggranularity == None:
                raise UnboundLocalError("addressinggranularity was not set yet")
        except UnboundLocalError as e:
            print("WishboneSlave.getAddressingGranularity:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self.__addressinggranularity

    def setWordSize(self, size):
        ''' set the size of a word in bits. It is required when you define
            addressinggranularity as word
            @param size: amount of bits a word represents
            @type size: Integer
            @raise TypeError: raised if parameter type mismatch is found
            @raise ValueError: raised if size is negative
            @rtype: Boolean
            @return: true on success, false otherwise
        '''
        try:
            if not isinstance(size, int):
                raise TypeError("size got the wrong type,"
                    +"excepted: Integer, got: "+str(type(size)))
            else:
                if size < 0:
                    raise ValueError("size of word cannot be negative")
        except TypeError as e:
            print("WishboneSlave.setWordSize:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneSlave.setWordSize:\n"
                +"\tValueError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self.__wordsize = size
        return True

    def getWordSize(self):
        ''' get the size of a word (amount of bits)
            @raise UnboundLocalError: raised if no state was assigned yet
            @rtype: Integer
            @return: size of a word on success, None otherwise
        '''
        try:
            if self.__wordsize == None:
                raise UnboundLocalError("wordsize was not set yet")
        except UnboundLocalError as e:
            print("WishboneSlave.getWordSize:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self.__wordsize

    def setHighestAddressBit(self, bit):
        ''' Set the highest bit of the address the slave uses
            @param bit: highest bit of the address
            @type bit: Integer
            @raise TypeError: raised if parameter type mismatch is found
            @rtype: Boolean
            @return: true on success, false otherwise
        '''
        try:
            if not isinstance(bit, int):
                raise TypeError("bit got the wrong type,"
                    +"excepted: Integer, got: "+str(type(bit)))
            else:
                if bit < 0:
                    raise ValueError("highest addressbit cannot be negative")
        except TypeError as e:
            print("WishboneComponent.setHighestAddressBit:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneSlave.setHighestAddressBit:\n"
                +"\tValueError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self.__addressbushigh = bit
        return True

    def getHighestAddressBit(self):
        ''' get the highest bit of the addressbus this slave requires
            @raise UnboundLocalError: raised if no state was assigned yet
            @rtype: Integer
            @return: highest bit of the addressbus on success, None otherwise
        '''
        try:
            if self.__addressbushigh == None:
                raise UnboundLocalError("highest addressbus bit was not set yet")
        except UnboundLocalError as e:
            print("WishboneComponent.getHighestAddressBit:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self.__addressbushigh

    def setLowestAddressBit(self, bit):
        ''' Set the lowest bit of the address the slave uses
            @param bit: lowest bit of the address
            @type bit: Integer
            @raise TypeError: raised if parameter type mismatch is found
            @rtype: Boolean
            @return: true on success, false otherwise
        '''
        try:
            if not isinstance(bit, int):
                raise TypeError("bit got the wrong type,"
                    +"excepted: Integer, got: "+str(type(bit)))
            else:
                if bit < 0:
                    raise ValueError("lowest addressbit cannot be negative")
        except TypeError as e:
            print("WishboneComponent.setLowestAddressBit:\n"
                +"\tTypeError occurred: "+e.args[0]+"\nstopping execution")
            return False
        except ValueError as e:
            print("WishboneSlave.setLowestAddressBit:\n"
                +"\tValueError occurred: "+e.args[0]+"\nstopping execution")
            return False

        self.__addressbuslow = bit
        return True

    def getLowestAddressBit(self):
        ''' get the lowest bit of the addressbus this slave requires
            @raise UnboundLocalError: raised if no state was assigned yet
            @rtype: Integer
            @return: lowest bit of the addressbus on success, None otherwise
        '''
        try:
            if self.__addressbuslow == None:
                raise UnboundLocalError("lowest addressbus bit was not set yet")
        except UnboundLocalError as e:
            print("WishboneComponent.getLowestAddressBit:\n"
                +"\tUnboundLocalError occurred: "+e.args[0]+"\nstopping execution")

        return self.__addressbuslow
