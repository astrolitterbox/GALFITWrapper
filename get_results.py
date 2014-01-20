import pyfits
from string import split
import csv
from fileOps import *

def split_errors(result_string):
  return result_string.split('+/-')


listFile = 'list.txt'
fileNames = np.genfromtxt(listFile, dtype='object')

def getMissingFiles(): 
	missingFiles = []
	for califa_id in range(1, 940):
		if "2D_"+str(califa_id)+".fits" in fileNames:
			print califa_id
		else:
			missingFiles.append(califa_id)


#ofile = open("Sersic_fit.csv", 'w')
#writer = csv.writer(ofile)
fo = open("Sersic_fit.csv", "a")
for califa_id in range(1, 940):
  zpt, mag, Reff, ra, dec, ba, pa, sky, run, rerun, field, camcol, runstr, field_str, center, inputFilename = galaxyParams(califa_id)
  print califa_id, ' GALAXY ', ra, dec
  try:
	  f = pyfits.open("output/2D_"+str(califa_id)+".fits")
	  y1, y1err = split_errors(f[2].header["1_YC"])
	  x1, x1err = split_errors(f[2].header["1_XC"])
	  ra1, dec1 = getWCSCoords(califa_id, runstr, camcol, field_str, (y1, x1))
	  ra_err1 = getAngularSize(califa_id, runstr, camcol, field_str, abs(float(y1err)))
	  dec_err1 = getAngularSize(califa_id, runstr, camcol, field_str, abs(float(x1err)))
	  rmag1, rmag1_err = split_errors(f[2].header["1_MAG"])
	  r1e, r1err = split_errors(f[2].header["1_RE"])
	  n1, n1err = split_errors(f[2].header["1_N"])
	  ba1, ba1err = split_errors(f[2].header["1_AR"])
	  pa1, pa1_err = split_errors(f[2].header["1_PA"])

	  y2, y2err = split_errors(f[2].header["1_YC"])
	  x2, x2err = split_errors(f[2].header["1_XC"])
	  ra2, dec2 = getWCSCoords(califa_id, runstr, camcol, field_str, (y2, x2))
	  ra_err2 = getAngularSize(califa_id, runstr, camcol, field_str, abs(float(y2err)))
	  dec_err2 = getAngularSize(califa_id, runstr, camcol, field_str, abs(float(x2err)))
	  rmag2, rmag2_err = split_errors(f[2].header["2_MAG"])
	  r2e, r2err = split_errors(f[2].header["2_RE"])
	  n2, n2err = split_errors(f[2].header["2_N"])

	  ba2, ba2err = split_errors(f[2].header["2_AR"])
	  pa2, pa2_err = split_errors(f[2].header["2_PA"])

  
	  sky, sky_err = split_errors(f[2].header["3_SKY"])
	  sky_ygrad, sky_ygrad_err = split_errors(f[2].header["3_DSDY"])
	  sky_xgrad, sky_xgrad_err = split_errors(f[2].header["3_DSDX"])
	  reduced_Chi2 = f[2].header["CHI2NU"]
	  flags = f[2].header["FLAGS"]


	  data = str(califa_id)+","+ "CALIFA"+str(califa_id).zfill(3)+", "+ str(ra1)+","+str(ra_err1)+","+str(dec1)+","+str(dec_err1)+","+str(rmag1)+","+ str(rmag1_err)+","+ str(r1e)+","+str(r1err)+","+ str(n1)+","+ str(n1err)+","+str(ba1)+","+str(ba1err)+","+str(pa1)+","+str(pa1_err)+","+ str(ra2)+","+ str(ra_err2)+","+ str(dec2)+","+str(dec_err2)+","+ str(rmag2)+","+ str(rmag2_err)+","+ str(r2e)+","+str(r2err)+","+ str(n2)+","+ str(n2err)+","+ str(ba2)+","+ str(ba2err)+","+ str(pa2)+","+ str(pa2_err)+","+ str(sky)+","+ str(sky_err)+","+str(sky_ygrad)+","+ str(sky_ygrad_err)+","+ str(sky_xgrad)+","+ str(sky_xgrad_err)+","+ str(reduced_Chi2)+","+ str(flags)+"\n"
	  fo.write(data)
  except (IOError, ValueError):
	  data = califa_id
	  fo.write(str(data)+"-999\n")
  
  #writer.writerow(data)
fo.close()  
