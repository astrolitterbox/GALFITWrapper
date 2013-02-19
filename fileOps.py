import pyfits
import numpy as np
from astLib import astWCS
import db
from utils import *

#settings
dbDir = '../db/'
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

def getMorphNumbers(morphtype, resolution):
  
  numbers = np.empty((morphtype.shape), dtype=int)
  if resolution == 'hubtype':

    numbers[np.where(morphtype == 'E0')] = 0
    numbers[np.where(morphtype == 'E1')] = 1
    numbers[np.where(morphtype == 'E2')] = 2
    numbers[np.where(morphtype == 'E3')] = 3
    numbers[np.where(morphtype == 'E4')] = 4  
    numbers[np.where(morphtype == 'E5')] = 5  
    numbers[np.where(morphtype == 'E6')] = 6
    numbers[np.where(morphtype == 'E7')] = 7
    numbers[np.where(morphtype == 'S0')] = 8
    numbers[np.where(morphtype == 'S0a')] = 9
    numbers[np.where(morphtype == 'Sa')] = 10
    numbers[np.where(morphtype == 'Sab')] = 11
    numbers[np.where(morphtype == 'Sb')] = 12 
    numbers[np.where(morphtype == 'Sbc')] = 13  
    numbers[np.where(morphtype == 'Sc')] = 14
    numbers[np.where(morphtype == 'Scd')] = 15
    numbers[np.where(morphtype == 'Sd')] = 16
    numbers[np.where(morphtype == 'Sdm')] = 17
    numbers[np.where(morphtype == 'Sm')] = 18
    numbers[np.where(morphtype == 'Ir')] = 19  
      
  elif resolution == 'barredness':
    numbers[np.where(morphtype == 'A')] = 0
    numbers[np.where(morphtype == 'AB')] = 1
    numbers[np.where(morphtype == 'B')] = 2

  elif resolution == 'merger':
   numbers[np.where(morphtype == 'I')] = 0
   numbers[np.where(morphtype == 'M')] = 1   
 
  return numbers
  
  
def galaxyParams(califa_id):
  	califa_id = str(califa_id)
	try:
		zpt = -1*(db.dbUtils.getFromDB('zpt', dbDir+'CALIFA.sqlite', 'r_tsfieldParams', ' where califa_id = '+califa_id)[0])
	except IndexError:
		zpt = 24.029 #mean of r band zpts -- NOTE that it's multiplied by -1, because SDSS stores them so
	print califa_id, 'CID', zpt, 'zpt'
	mag = db.dbUtils.getFromDB('r', dbDir+'CALIFA.sqlite', 'gc_results', ' where califa_id = '+califa_id)[0]
	Reff = 0.8*db.dbUtils.getFromDB('hlma', dbDir+'CALIFA.sqlite', 'gc_results', ' where califa_id = '+califa_id)[0]
	ra = db.dbUtils.getFromDB('ra', dbDir+'CALIFA.sqlite', 'mothersample', ' where califa_id = '+califa_id)[0]
	dec = db.dbUtils.getFromDB('dec', dbDir+'CALIFA.sqlite', 'mothersample', ' where califa_id = '+califa_id)[0]

	ba = db.dbUtils.getFromDB('ba', dbDir+'CALIFA.sqlite', 'nadine', ' where califa_id = '+califa_id)[0]
	pa = db.dbUtils.getFromDB('pa', dbDir+'CALIFA.sqlite', 'nadine', ' where califa_id = '+califa_id)[0]
	sky = db.dbUtils.getFromDB('gc_sky', dbDir+'CALIFA.sqlite', 'gc_results', ' where califa_id = '+califa_id)[0]
	run = db.dbUtils.getFromDB('run', dbDir+'CALIFA.sqlite', 'mothersample', ' where califa_id = '+califa_id)[0]
	rerun = db.dbUtils.getFromDB('rerun', dbDir+'CALIFA.sqlite', 'mothersample', ' where califa_id = '+califa_id)[0]
	field = db.dbUtils.getFromDB('field', dbDir+'CALIFA.sqlite', 'mothersample', ' where califa_id = '+califa_id)[0]	
	camcol = str(db.dbUtils.getFromDB('camcol', dbDir+'CALIFA.sqlite', 'mothersample', ' where califa_id = '+califa_id)[0])
	runstr = run2string(run)
	field_str = field2string(field)	
	center = getPixelCoords(califa_id, runstr, camcol, field_str, (ra, dec))	
	inputFilename = getFilledUrl(califa_id, runstr, camcol, field_str)
	return zpt, mag, Reff, ra, dec, ba, pa, sky, run, rerun, field, camcol, runstr, field_str, center, inputFilename


def getWCSCoords(ID, runstr, camcol, field_str, centerCoords):
    WCS=astWCS.WCS(getSDSSUrl(ID, runstr, camcol, field_str))
    wcsCoords = WCS.pix2wcs(float(centerCoords[1]), float(centerCoords[0]))
    return wcsCoords
    
def getPixelCoords(ID, runstr, camcol, field_str, centerCoords):
    WCS=astWCS.WCS(getSDSSUrl(ID, runstr, camcol, field_str))
    #print 'centerCoords', centerCoords
    pixelCoords = WCS.wcs2pix(float(centerCoords[0]), float(centerCoords[1]))
    #print 'pixCoords', pixelCoords
    return (pixelCoords[1], pixelCoords[0]) #y -- first, x axis -- second

def getAngularSize(ID, runstr, camcol, field_str, angle):
    #returns angular size in arcseconds -- not in degrees, as the original WCS!
    WCS = astWCS.WCS(getSDSSUrl(ID, runstr, camcol, field_str))
    angularSize = WCS.getPixelSizeDeg() * angle * 3600
    return angularSize

def getFilledUrl(ID, runstr, camcol, field_str):
      dupeList = [162, 164, 249, 267, 319, 437, 445, 464, 476, 477, 480, 487, 498, 511, 537, 570, 598, 616, 634, 701, 767, 883, 939]
      if band == 'r':
        fpCFile = dataDir+'/filled2/fpC-'+runstr+'-'+band+camcol+'-'+field_str+'.fits'
        if (int(ID)) in dupeList:
                fpCFile = dataDir+'/filled3/fpC-'+runstr+'-'+band+camcol+'-'+field_str+'.fits'
      else:
              fpCFile = dataDir+'/filled_'+band+'/fpC-'+runstr+'-'+band+camcol+'-'+field_str+'.fits'
              if(int(ID)) in dupeList:
                fpCFile = fpCFile+'B'
      return fpCFile
      
def getSDSSUrl(ID, runstr, camcol, field_str):
      fpCFile = dataDir+'/SDSS/'+band+'/fpC-'+runstr+'-'+band+camcol+'-'+field_str+'.fit.gz'
      return fpCFile
