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

califa_ids = db.dbUtils.getFromDB('califa_id', dbDir+'CALIFA.sqlite', 'mothersample', ' where califa_id > 937')

for califa_id in califa_ids:
	print califa_id
	
	califa_id = str(califa_id)
	ofileName = "input/galfit_"+califa_id
	ofile = open(ofileName, 'wb')
	writer = csv.writer(ofile)

	try:
		zpt = db.dbUtils.getFromDB('zpt', dbDir+'CALIFA.sqlite', 'r_tsfieldParams', ' where califa_id = '+califa_id)[0]
	except IndexError:
		zpt = -24.029 #mean of r band zpts
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
	outputFilename = 'input/out_'+califa_id 
	#print originalFilename, inputFilename
	#editHeader(inputFilename, originalFilename, zpt)


	ControlLines = ["================================================================================", "# IMAGE and GALFIT CONTROL PARAMETERS", 
	"A) "+inputFilename+"      # Input data image (FITS file)",
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
	  writer.writerow([line])
	    
	InitialLines = ["# INITIAL FITTING PARAMETERS", "# ------------------------------------------------------------------------------",
	"# Component number: 1",
	 "0) sersic                 #  Component type", 
	 "1) "+center[1]+" "+center[0]+" 1 1  #  Position x, y", 
	 "3) "+mag+"     1          #  Integrated magnitude ",
	 "4) "+Reff+"     1          #  R_e (effective radius)   [pix]",
	 "5) 2.5      1          #  Sersic index n (de Vaucouleurs n=4) ",
	 "6) 0.0000      0          #     ----- ",
	 "7) 0.0000      0          #     ----- ",
	 "8) 0.0000      0          #     ----- ",
	 "9) "+ba+"      1          #  Axis ratio (b/a)",   
	"10) "+pa+"     1          #  Position angle (PA) [deg: Up=0, Left=90]", 
	 "Z) 0                      #  Skip this model in output image?  (yes=1, no=0)"]

	for line in InitialLines:
	  print "out", line
	  writer.writerow([line])


	InitialSkyLines = ["# Component number: 2", 
	 "0) sky                    #  Component type",
	 "1) "+sky+"    1          #  Sky background at center of fitting region [ADUs]",
	 "2) 0     1       #  dsky/dx (sky gradient in x)     [ADUs/pix]",
	 "3) 0     1       #  dsky/dy (sky gradient in y)     [ADUs/pix]",
	 "Z) 0                      #  Skip this model in output image?  (yes=1, no=0)",
	"================================================================================"]

	for line in InitialSkyLines:
	  print "out", line
	  writer.writerow([line])
	ofile.close()
