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
  print ra, dec
  f = pyfits.open("output/"+str(califa_id)+".fits")
  y, yerr = split_errors(f[2].header["1_YC"])
  x, xerr = split_errors(f[2].header["1_XC"])
  ra, dec = getWCSCoords(califa_id, runstr, camcol, field_str, (y, x))
  ra_err = getAngularSize(califa_id, runstr, camcol, field_str, abs(float(yerr)))
  dec_err = getAngularSize(califa_id, runstr, camcol, field_str, abs(float(xerr)))
  rmag, rmag_err = split_errors(f[2].header["1_MAG"])
  re, rerr = split_errors(f[2].header["1_RE"])
  n, nerr = split_errors(f[2].header["1_N"])
  pa, pa_err = split_errors(f[2].header["1_PA"])
  sky, sky_err = split_errors(f[2].header["2_SKY"])
  sky_ygrad, sky_ygrad_err = split_errors(f[2].header["2_DSDY"])
  sky_xgrad, sky_xgrad_err = split_errors(f[2].header["2_DSDX"])
  reduced_Chi2 = f[2].header["CHI2NU"]
  flags = f[2].header["FLAGS"]


  writer.writerow((califa_id, "CALIFA"+str(califa_id).zfill(3), ra, ra_err,  dec, dec_err, rmag, rmag_err, re, rerr, n, nerr, pa, pa_err, sky, sky_err, sky_ygrad, sky_ygrad_err, sky_xgrad, sky_xgrad_err, reduced_Chi2, flags))
ofile.close()  