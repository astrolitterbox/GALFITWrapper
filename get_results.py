import pyfits
from string import split
import csv
from fileOps import *

def split_errors(result_string):
  return result_string.split('+/-')


ofile = open("Sersic_fit.csv", 'wb')
writer = csv.writer(ofile)

for califa_id in range(1, 940):
  zpt, mag, Reff, ra, dec, ba, pa, sky, run, rerun, field, camcol, runstr, field_str, center, inputFilename = galaxyParams(califa_id)
  print califa_id, ' GALAXY ', ra, dec
  f = pyfits.open("output/"+str(califa_id)+".fits")
  y1, y1err = split_errors(f[2].header["1_YC"])
  x1, x1err = split_errors(f[2].header["1_XC"])
  ra1, dec1 = getWCSCoords(califa_id, runstr, camcol, field_str, (y1, x1))
  ra_err1 = getAngularSize(califa_id, runstr, camcol, field_str, abs(float(y1err)))
  dec_err1 = getAngularSize(califa_id, runstr, camcol, field_str, abs(float(x1err)))
  rmag1, rmag1_err = split_errors(f[2].header["1_MAG"])
  r1e, r1err = split_errors(f[2].header["1_RE"])
  n1, n1err = split_errors(f[2].header["1_N"])
  pa1, pa1_err = split_errors(f[2].header["1_PA"])

  y2, y2err = split_errors(f[2].header["1_YC"])
  x2, x2err = split_errors(f[2].header["1_XC"])
  ra2, dec2 = getWCSCoords(califa_id, runstr, camcol, field_str, (y2, x2))
  ra_err2 = getAngularSize(califa_id, runstr, camcol, field_str, abs(float(y2err)))
  dec_err2 = getAngularSize(califa_id, runstr, camcol, field_str, abs(float(x2err)))
  rmag2, rmag2_err = split_errors(f[2].header["2_MAG"])
  r2e, r2err = split_errors(f[2].header["2_RE"])
  n2, n2err = split_errors(f[2].header["2_N"])
  pa2, pa2_err = split_errors(f[2].header["2_PA"])

  
  sky, sky_err = split_errors(f[2].header["2_SKY"])
  sky_ygrad, sky_ygrad_err = split_errors(f[2].header["2_DSDY"])
  sky_xgrad, sky_xgrad_err = split_errors(f[2].header["2_DSDX"])
  reduced_Chi2 = f[2].header["CHI2NU"]
  flags = f[2].header["FLAGS"]


  data = califa_id, "CALIFA"+str(califa_id).zfill(3), ra1, ra_err1,  dec1, dec_err1, rmag1, rmag1_err, r1e, r1err, n1, n1err, pa1, pa1_err, ra2, ra_err2,  dec2, dec_err2, rmag2, rmag2_err, r2e, r2err, n2, n2err, pa2, pa2_err, sky, sky_err, sky_ygrad, sky_ygrad_err, sky_xgrad, sky_xgrad_err, reduced_Chi2, flags

  writer.writerow(())
ofile.close()  