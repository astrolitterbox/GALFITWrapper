import pyfits 
import sys
from fileOps import *

#utility script for writing necessary info to a header from the original SDSS file

def editHeader(filename, originalFile):
	OriginalHDUList = pyfits.open(originalFile)
	OriginalHeader = OriginalHDUList[0].header
	HDUList = pyfits.open(fileName, mode = 'update')
	HDUList[0].header = OriginalHeader
	HDUList[0].header["SOFTBIAS"] = 0
	HDUList[0].header["BZERO"] = 0
	HDUList[0].header["ZPT"] = zpt
	print HDUList[0].header
	HDUList.flush()
