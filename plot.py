from utils import *
import matplotlib.pyplot as plt
import db
import numpy as np
import matplotlib
from fileOps import *


dbDir = '../db/'

v22_ids = db.dbUtils.getFromDB('califa_id', dbDir+'CALIFA.sqlite', 'vf')

v22_ids = sqlify(v22_ids)

n = db.dbUtils.getFromDB('n', dbDir+'CALIFA.sqlite', 'galfit')
g = np.asarray(db.dbUtils.getFromDB('g', dbDir+'CALIFA.sqlite', 'gc_results'))
r = np.asarray(db.dbUtils.getFromDB('r', dbDir+'CALIFA.sqlite', 'gc_results'))
Mr = np.asarray(db.dbUtils.getFromDB('r', dbDir+'CALIFA.sqlite', 'kcorrect'))
v22 = np.asarray(db.dbUtils.getFromDB('v22', dbDir+'CALIFA.sqlite', 'vf'))

n_vf = db.dbUtils.getFromDB('n', dbDir+'CALIFA.sqlite', 'galfit', ' where califa_id in '+v22_ids)


print v22.shape
#morph = (db.dbUtils.getFromDB())
col = g-r
#n = np.reshape(n, (n.shape[0], 1))
#print n.shape

fig = plt.figure()
plt.hist(n, bins = 30, color='royalBlue')
plt.xlabel(r"S$\'{e}$rsic n")
plt.ylabel("No. of galaxies")
#plt.savefig("img/n_hist")



fig = plt.figure()
p = plt.scatter(col, Mr, c=np.clip(n, 0, 6))
plt.ylabel(r"M$_r$")
plt.xlabel("g-r colour")
plt.xlim(0, 1.5)
colb = plt.colorbar(p)
colb.ax.set_ylabel(r"S$\'{e}$rsic n")
#plt.savefig("img/n_colour")


fig = plt.figure()
p = plt.scatter(n_vf, v22, c=np.clip(n_vf, 0, 6))
plt.ylabel(r"V$_{2.2}$")
plt.xlabel("n")
plt.ylim(0, 400)
colb = plt.colorbar(p)
colb.ax.set_ylabel(r"S$\'{e}$rsic n")
plt.savefig("img/n_v22")

  
 
Hubtype = np.asarray(decodeU(db.dbUtils.getFromDB('Hubtype', dbDir+'CALIFA.sqlite', 'morph')))
HubSubType = np.asarray(decodeU(db.dbUtils.getFromDB('HubSubtype', dbDir+'CALIFA.sqlite', 'morph')))


morphtypes = np.empty((Hubtype.shape[0], 1), dtype = 'object')
for i, galaxy in enumerate(Hubtype):
  morphtypes[i] = galaxy+HubSubType[i]
#print morphtypes

resolution = 'hubtype'

morph = getMorphNumbers(morphtypes, resolution)

types = ['EO', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'S0', 'S0a', 'Sa', 'Sab', 'Sb', 'Sbc', 'Sc', 'Scd', 'Sd', 'Sdm', 'Sm', 'Ir']

print morph


clipped_col = np.clip(col, np.mean(col)-2*np.std(col), np.mean(col)+2*np.std(col))

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111)
p = plt.scatter(morph, n, c=clipped_col, alpha=0.9, s=30)
plt.ylabel(r"S$\'{e}$rsic n")
plt.xlabel("Hubble type")
plt.xlim(-0.2, 20)
plt.ylim(-0, 8)
#Minor_locator = matplotlib.ticker.FixedLocator(morph)
Minor_formatter = matplotlib.ticker.FixedFormatter(types)
majorLocator = matplotlib.ticker.MultipleLocator(1)
cbar = plt.colorbar(p)

#minorLocator = matplotlib.ticker.MultipleLocator(1)
#ax.xaxis.set_minor_locator(minorLocator)
ax.xaxis.set_major_locator(majorLocator)
ax.xaxis.set_major_formatter(Minor_formatter)

cbar.ax.set_ylabel("g-r color")
plt.savefig("img/n_Hubtype")