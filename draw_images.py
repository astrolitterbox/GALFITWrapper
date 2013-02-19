#generates images
import numpy as np
import matplotlib.pyplot as plt
import pyfits
import matplotlib.cm as cm
import db
from fileOps import *
dbDir = '../db/'

def cut_out(inputImage, size, center):
    Ymin = center[0] - size
    Ymax = center[0] + size
    Xmin = center[1] - size
    Xmax = center[1] + size
    try:
      output = inputImage[Ymin:Ymax, Xmin:Xmax]
    except IndexError:
      print 'nesueina!'
    return output

def clip_image(inputImage):
    sigma = np.std(inputImage)
    mean = np.mean(inputImage)
    ret = np.clip(inputImage, mean-3*sigma, mean+3*sigma)
    return ret

for califa_id in range(651, 940):
  zpt, mag, Reff, ra, dec, ba, pa, sky, run, rerun, field, camcol, runstr, field_str, center, inputFilename = galaxyParams(califa_id)
  f = pyfits.open("output/"+str(califa_id)+".fits")
  inputImage = f[1].data
  modelImage = f[2].data
  residualImage = f[3].data
  
  fig = plt.figure(figsize = (10, 5))
  ax0 = fig.add_subplot(131)
  
  p = ax0.imshow(clip_image(cut_out(inputImage, 100, center)), cmap=cm.hot, interpolation='nearest')
  #p.set_clim(-3,1000)
  ax0.xaxis.set_visible(False)
  ax0.yaxis.set_visible(False)
  cb = plt.colorbar(p, shrink=0.455)

  ax1 = fig.add_subplot(132)
  p = ax1.imshow(clip_image(cut_out(modelImage, 100, center)), cmap=cm.hot, interpolation='nearest')
  ax1.xaxis.set_visible(False)
  ax1.yaxis.set_visible(False)
  cb = plt.colorbar(p, shrink=0.455)

  ax2 = fig.add_subplot(133)
  p = ax2.imshow(clip_image(cut_out(residualImage, 100, center)), cmap=cm.hot, interpolation='nearest')
  ax2.xaxis.set_visible(False)
  ax2.yaxis.set_visible(False) 
  cb = plt.colorbar(p, shrink=0.455)
  
  plt.savefig("img/"+str(califa_id)+".pdf", bbox_inches="tight", dpi=72)
  
  f.close()
    
  
  
