import pyfits
from string import split

def split_errors(result_string):
  return result_string.split('+/-')


for i in range(938, 940):
  f = pyfits.open("output/"+str(i)+".fits")
  y = f[2].header["1_YC"]
  x = f[2].header["1_XC"]
  r = f[2].header["1_MAG"]
  re = f[2].header["1_RE"]
  n = f[2].header["1_N"]
  pa = f[2].header["1_PA"]
  sky = f[2].header["2_SKY"]
  sky_ygrad = f[2].header["2_DSDY"]
  sky_xgrad = f[2].header["2_DSDX"]
  reduced_Chi2 = f[2].header["CHI2NU"]
  flags = f[2].header["FLAGS"]
  
print split_errors(y)

#y, x, r, re, n, pa, sky, sky_ygrad, sky_xgrad, reduced_Chi2, flags
  