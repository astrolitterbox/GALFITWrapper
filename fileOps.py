import pyfits
import numpy as np
from astLib import astWCS

band = 'r'
#dataDir = '/media/46F4A27FF4A2713B_/work2/data'
dataDir = '../data'

def getInputFile(i, band):
    #print 'filename:', GalaxyParameters.getFilledUrl(listFile, dataDir, i)
    inputFile = pyfits.open(GalaxyParameters.getFilledUrl(i, band))
    inputImage = inputFile[0].data
    if band != 'r' or (i == 882) or (i == 576):
       inputImage-=1000
    #print 'opened the input file'
    return inputImage


    
def getPixelCoords(ID, runstr, camcol, field_str, centerCoords):
    WCS=astWCS.WCS(getSDSSUrl(ID, runstr, camcol, field_str))
    print 'centerCoords', centerCoords
    pixelCoords = WCS.wcs2pix(centerCoords[0], centerCoords[1])
    print 'pixCoords', pixelCoords
    out = [ID, centerCoords[0], centerCoords[1], pixelCoords[0], pixelCoords[1]]
    #utils.writeOut(out, 'coords.csv')
    return (pixelCoords[1], pixelCoords[0]) #y -- first, x axis -- second

def getFilledUrl(ID, runstr, camcol, field_str):
      dupeList = [162, 164, 249, 267, 319, 437, 445, 464, 476, 477, 480, 487, 498, 511, 537, 570, 598, 616, 634, 701, 767, 883, 939]
      if band == 'r':
        fpCFile = dataDir+'/filled2/fpC-'+runstr+'-'+band+camcol+'-'+field_str+'.fits'
        if (int(ID) +1) in dupeList:
                fpCFile = dataDir+'/filled3/fpC-'+runstr+'-'+band+camcol+'-'+field_str+'.fits'
      else:
              fpCFile = dataDir+'/filled_'+band+'/fpC-'+runstr+'-'+band+camcol+'-'+field_str+'.fits'
              if(int(ID) + 1) in dupeList:
                fpCFile = fpCFile+'B'
      return fpCFile
      
def getSDSSUrl(ID, runstr, camcol, field_str):
      fpCFile = dataDir+'/SDSS/'+band+'/fpC-'+runstr+'-'+band+camcol+'-'+field_str+'.fit.gz'
      return fpCFile
