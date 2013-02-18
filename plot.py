from utils import *
import matplotlib.pyplot as plt
import db
import numpy as np
from matplotlib import colors

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
c = plt.colorbar(p)
c.ax.set_ylabel(r"S$\'{e}$rsic n")
#plt.savefig("img/n_colour")


fig = plt.figure()
p = plt.scatter(n_vf, v22, c=np.clip(n_vf, 0, 6))
plt.ylabel(r"V$_{2.2}$")
plt.xlabel("n")
plt.ylim(0, 400)
c = plt.colorbar(p)
c.ax.set_ylabel(r"S$\'{e}$rsic n")
plt.savefig("img/n_v22")