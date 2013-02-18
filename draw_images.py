#generates LaTeX source of thumbnails
import numpy as np
import matplotlib.pyplot as plt
import pyfits
import matplotlib.cm as cm

def clip_image(inputImage):
    sigma = np.std(inputImage)
    mean = np.mean(inputImage)
    ret = np.clip(inputImage, mean-3*sigma, mean+3*sigma)
    return ret

for califa_id in range(1, 2):
  f = pyfits.open("output/"+str(califa_id)+".fits")
  inputImage = f[1].data
  modelImage = f[2].data
  residualImage = f[3].data
  
  fig = plt.figure(figsize = (8, 5))
  ax0 = fig.add_subplot(131)
  p = ax0.imshow(clip_image(inputImage), cmap=cm.hot, interpolation='nearest')
  #p.set_clim(-3,1000)
  ax0.xaxis.set_visible(False)
  ax0.yaxis.set_visible(False)

  ax1 = fig.add_subplot(132)
  ax1.imshow(clip_image(modelImage), cmap=cm.hot)
  ax1.xaxis.set_visible(False)
  ax1.yaxis.set_visible(False)

  ax2 = fig.add_subplot(133)
  ax2.imshow(clip_image(residualImage), cmap=cm.hot)
  ax2.xaxis.set_visible(False)
  ax2.yaxis.set_visible(False)
  
  plt.savefig("img/"+str(califa_id), bbox_inches="tight")
    
  
  
