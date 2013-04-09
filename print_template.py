import pyfits, numpy as np, db

from fileOps import *
import sys
from string import *
from string import Template
import csv
from editHeader import *




califa_ids = db.dbUtils.getFromDB('califa_id', dbDir+'CALIFA.sqlite', 'mothersample')

#califa_ids = [164, 319, 437, 445, 464, 476, 477, 480, 487, 498, 511, 537, 570, 598, 616, 634, 701, 767, 883, 939, 161, 163, 248, 266, 318, 436, 444, 463, 475, 476, 479, 486, 497, 510, 536,569, 597, 615, 633, 700, 766, 882, 938]

#califa_ids = [1, 2]


for califa_id in califa_ids:
	print califa_id
	ofileName = "input/galfit_"+str(califa_id)
	ofile = open(ofileName, 'wb')
	zpt, mag, Reff, ra, dec, ba, pa, sky, run, rerun, field, camcol, runstr, field_str, center, inputFilename = galaxyParams(califa_id)
	outputFilename = '../output/2D_'+str(califa_id)

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
	 "Z) 0                      #  Skip this model in output image?  (yes=1, no=0)",
	"# Component number: 2",
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

	InitialSkyLines = ["# Component number: 3", 
	 "0) sky                    #  Component type",
	 "1) "+str(sky)+"    1          #  Sky background at center of fitting region [ADUs]",
	 "2) 0     1       #  dsky/dx (sky gradient in x)     [ADUs/pix]",
	 "3) 0     1       #  dsky/dy (sky gradient in y)     [ADUs/pix]",
	 "Z) 0                      #  Skip this model in output image?  (yes=1, no=0)",
	"================================================================================"]

	for line in InitialSkyLines:
	  print "out", line
	  writeOut([line], ofileName)
	  ofile.write(line+"\n")
	ofile.close()
