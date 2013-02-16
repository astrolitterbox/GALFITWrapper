import pyfits 
import sys
from fileOps import *

#utility script for writing necessary info to a header from the original SDSS file

def editHeader(fileName, originalFile, zpt):
	OriginalHDUList = pyfits.open(originalFile)
	OriginalHeader = OriginalHDUList[0].header
	HDUList = pyfits.open(fileName, mode = 'update')
	HDUList[0].header = OriginalHeader
	HDUList[0].header["SOFTBIAS"] = 0
	HDUList[0].header["BZERO"] = 0
	HDUList[0].header.append(("ZPT", zpt))
	print OriginalHeader
	HDUList.flush()
