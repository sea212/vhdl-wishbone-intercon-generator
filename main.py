#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
from time import time

# add custom libraries
path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'libs'))
if not path in sys.path:
    print(path)
    sys.path.insert(1, path)
del path

from wb_file_manager import WishboneFileManager

''' this programm controlls the general flow '''

__author__ = "Harald Heckmann"
__copyright__ = "Copyright 2016"
__credits__ = ["Prof. Dr. Steffen Reith (steffen.reith@hs-rm.de)", \
                "Harald Heckmann (harald.heckmann@student.hs-rm.de)"]
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Harald Heckmann"
__email__ = "harald.heckmann@student.hs-rm.de"
__status__ = "Development (alpha)"

if __name__ == '__main__':
    start = time()
    terminate = "success"

    try:
        wbmngr = WishboneFileManager()
        wbmngr.parse()
        wbmngr.printConfigContent()
        wbmngr.generateIntercon()
    except Exception as e:
        terminate = "failure"
        print("\nmain: "+e.args[0])


    timedif = time()-start
    testdif = timedif*1000000
    print("\n")
    if (testdif > 1000000): print("Execution time: %f seconds" % (timedif*1000000))
    elif (testdif > 1000): print("Execution time: %f milliseconds" % (timedif*1000))
    else: print("Execution time: %f microseconds" % testdif)

    print("Exit status: "+terminate)
