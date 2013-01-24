#Comparison of griddata with smear based on http://matplotlib.org/examples/pylab_examples/griddata_demo.html

from numpy.random import uniform, seed
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import numpy as np
from smear import Interpolator

# make up data.
#npts = int(raw_input('enter # of random points to plot:'))
seed(0)
npts = 200
x = uniform(-2,2,npts)
y = uniform(-2,2,npts)
z = x*np.exp(-x**2-y**2)
# define grid.
xi = np.linspace(-2.1,2.1,100)
yi = np.linspace(-2.1,2.1,200)

# need to do a little bit of extra work to get the data in the form smear needs
# since griddata automatically does the meshgrid internally
xi2, yi2 = np.meshgrid(xi,yi)
points = np.vstack((x, y)).T
interp_points = np.vstack((xi2.ravel(), yi2.ravel())).T

# interpolate the data.
zi = griddata(x,y,z,xi,yi,interp='linear')
fn = Interpolator(points, z)
zi_idw = fn(interp_points, method='idw', nnear=10) #using inverse distance wieghting with a nieghborhood of 10 points


# contour the gridded data from griddata, plotting dots at the nonuniform data points.
plt.figure()
CS = plt.contour(xi,yi,zi,15,linewidths=0.5,colors='k')
CS = plt.contourf(xi,yi,zi,15,cmap=plt.cm.rainbow,
                  vmax=abs(zi).max(), vmin=-abs(zi).max())
plt.colorbar() # draw colorbar
# plot data points.
plt.scatter(x,y,marker='o',c='b',s=5,zorder=10)
plt.xlim(-2,2)
plt.ylim(-2,2)
plt.title('griddata linear test (%d points)' % npts)


# contour the gridded data from smear, plotting dots at the nonuniform data points.
# this will look different from griddata because we are using idw rather than linear
# idw doesn't have the convex hull issue.

plt.figure()
CS = plt.contour(xi,yi,zi_idw.reshape(xi2.shape),15,linewidths=0.5,colors='k')
CS = plt.contourf(xi,yi,zi_idw.reshape(xi2.shape),15,cmap=plt.cm.rainbow,
                  vmax=abs(zi_idw).max(), vmin=-abs(zi_idw).max())
plt.colorbar() # draw colorbar
# plot data points.
plt.scatter(x,y,marker='o',c='b',s=5,zorder=10)
plt.xlim(-2,2)
plt.ylim(-2,2)
plt.title('smear idw test (%d points)' % npts)

plt.show()