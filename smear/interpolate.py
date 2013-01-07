import numpy as np
from scipy.interpolate.interpnd import LinearNDInterpolator, CloughTocher2DInterpolator

from scipy.spatial import cKDTree as KDTree

class Interpolator:
    def __init__(self, points, values, ellipsivity=1., leafsize=10):
        assert len(points) == len(values), "len(points) %d != len(values) %d" % (len(points), len(values))
        self.points = points
        if ellipsivity!=1.:
            points[:,0] = points[:,0]*ellipsivity

        self.tree = KDTree(points, leafsize=leafsize )  # build the tree
        self.values = values

    def __call__(self, xi, method='nearest', nnear=6, eps=0, threshold=1e-10, **kwargs):

        if method == 'nearest':
            dist, ix = self.tree.query(xi)
            return self.values[ix,]
        elif method in ('linear', 'cubic', 'idw'):
            #todo raise error if nnear too small for interp type.
            dist, ix = self.tree.query(xi, k=nnear, eps=eps )

            #directly assign nearest nieghbour for xi that are closer than threshold to a point
            interpolated_values = np.zeros((len(dist),) + np.shape(self.values[0]))
            below_threshold = dist[:,0] < threshold
            interpolated_values[below_threshold] = self.values[ix[below_threshold][:,0],]

            n_interp = 0
            above_threshold = interpolated_values[~below_threshold,:]
            interpolator_fn = getattr(self, '_' + method)
            for dist, ix in zip(dist[~below_threshold], ix[~below_threshold]):                
                above_threshold[n_interp] = interpolator_fn(dist, ix, n_interp, xi, **kwargs)
                n_interp += 1

            interpolated_values[~below_threshold,:] = above_threshold

            return interpolated_values if xi.ndim > 1 else interpolated_values[0]
        
        else:
            raise ValueError("Unknown interpolation method %s." % (method))
        
    def _cubic(self, dist, ix, n_interp, xi):
        return CloughTocher2DInterpolator(self.points[ix], self.values[ix])(np.array([xi[n_interp]]))

    def _idw(self, dist, ix, n_interp, xi, power=1):
        """Inverse Distance Weighted Interpolation.

        Parameters
        ----------
        X_new: numpy array, shape = (n, 2) 
            Target interpolation points. 

        eps : nonnegative float, optional (default=0)
            Return approximate nearest neighbors; the kth returned value is 
            guaranteed to be no further than (1+eps) times the distance to the real kth nearest neighbor.

        nnear: integer, optional (default = 6)
            number of nearest neighbours to use for each target point 

        power: integer

        threshold: nonnegative float
            threshold distance below which target points are considered equivalent to existing point and values used directly 

        Examples
        --------
        >>> from sklearn.neighbors.nearest_centroid import NearestCentroid
        [1]

        References
        ----------
        http://stackoverflow.com/questions/3104781/inverse-distance-weighted-idw-interpolation-with-python
        """
        
        w = 1 / dist**power
        w /= np.sum(w)

        return np.dot(w, self.values[ix,])

    def _linear(self, dist, ix, n_interp, xi):
        return LinearNDInterpolator(self.points[ix], self.values[ix])(np.array([xi[n_interp]]))
        
    def _nearest(self, xi):
        dist, ix = self.tree.query(xi)
        return self.values[ix,]
