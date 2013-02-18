import pyfits, numpy as np, db
from utils import *
from fileOps import *
import sys
from string import *
from string import Template
import csv
from editHeader import *

#settings
dbDir = '../db/'

#califa_ids = db.dbUtils.getFromDB('califa_id', dbDir+'CALIFA.sqlite', 'mothersample')

#califa_ids = [164, 319, 437, 445, 464, 476, 477, 480, 487, 498, 511, 537, 570, 598, 616, 634, 701, 767, 883, 939, 161, 163, 248, 266, 318, 436, 444, 463, 475, 476, 479, 486, 497, 510, 536,569, 597, 615, 633, 700, 766, 882, 938]



for califa_id in califa_ids:
	print califa_id
	
	califa_id = str(califa_id)
	ofileName = "input/galfit_"+califa_id
	ofile = open(ofileName, 'wb')
	#writer = csv.writer(ofile, quoting=csv.QUOTE_NONE)

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
	#originalFilename = getSDSSUrl(califa_id, runstr, camcol, field_str)
	outputFilename = '../output/'+califa_id 
	#print originalFilename, inputFilename
	#editHeader(inputFilename, originalFilename, zpt)


	ControlLines = ["================================================================================", "# IMAGE and GALFIT CONTROL PARAMETERS", 
	"A) ../"+inputFilename+"      # Input data image (FITS file)",
	"B) "+outputFilename+".fits        # Output data image block", 
	"C) # Sigma image name (made from data if blank or none) ", 
	"D) # Input PSF image and (optional) diffusion kernel", 
	"E) 1 # PSF fine sampling factor relative to data ", 
	"F) # Bad pixel mask (FITS image or ASCII coord list)",
	"G) none # File with parameter constraints (ASCII file)", 
	"H) 1    2048 1    1489 # Image region to fit (xmin xmax ymin ymax)",
	"I) 30     30   # Size of the convolution box (x y)", 
	"J) "+str(zpt)+"   # Magnitude photometric zeropoint", 
	"K) 0.396  0.396 # Plate scale (dx dy)   [arcsec per pixel]", 
	"O) regular  # Display type (regular, curses, both) ", 
	"P) 0 # Choose: 0=optimize, 1=model, 2=imgblock, 3=subcomps"]

	for line in ControlLines:
	  print "out", line
	  #writer.writerow([line])
	  ofile.write(line+"\n")
	    
	InitialLines = ["# INITIAL FITTING PARAMETERS", "# ------------------------------------------------------------------------------",
	"# Component number: 1",
	 "0) sersic                 #  Component type", 
	 "1) "+str(center[1])+" "+str(center[0])+" 1 1  #  Position x, y", 
	 "3) "+str(mag)+"     1          #  Integrated magnitude ",
	 "4) "+str(Reff)+"     1          #  R_e (effective radius)   [pix]",
	 "5) 2.5      1          #  Sersic index n (de Vaucouleurs n=4) ",
	 "6) 0.0000      0          #     ----- ",
	 "7) 0.0000      0          #     ----- ",
	 "8) 0.0000      0          #     ----- ",
	 "9) "+str(ba)+"      1          #  Axis ratio (b/a)",   
	"10) "+str(pa)+"     1          #  Position angle (PA) [deg: Up=0, Left=90]", 
	 "Z) 0                      #  Skip this model in output image?  (yes=1, no=0)"]

	for line in InitialLines:
	  print "out", line
	  #writer.writerow([line])

	  ofile.write(line+"\n")

	InitialSkyLines = ["# Component number: 2", 
	 "0) sky                    #  Component type",
	 "1) "+str(sky)+"    1          #  Sky background at center of fitting region [ADUs]",
	 "2) 0     1       #  dsky/dx (sky gradient in x)     [ADUs/pix]",
	 "3) 0     1       #  dsky/dy (sky gradient in y)     [ADUs/pix]",
	 "Z) 0                      #  Skip this model in output image?  (yes=1, no=0)",
	"================================================================================"]

	for line in InitialSkyLines:
	  print "out", line
	  #writeOut([line], ofileName)
	  ofile.write(line+"\n")
	ofile.close()
