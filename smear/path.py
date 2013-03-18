"""
module for cleaning up paths, i.e. boat/vehicle tracks etc
"""
import numpy as np

# function for 1D interpolation of a curved line or boat track.
def densify_path(path, spacing, values=None):
    """
    returns a new path with evenly spaced points <= spacing
    distance between the original set of points. It does not move
    existing points. path and values should be (n, 2) numpy arrays.
    Points are linearly interpolated between existing points. path 
    is an ordered set of xy points.
    """

    if path.shape[1]!=2:
        raise ValueError("Found path array with shape %s. Expected shape (n, 2)"
                             % (str(path.shape)))

    if values is not None:
        if len(values)!=len(path):
            raise  ValueError("Length of path and values arrays must match")

    # make a copy for output
    dense_path = path[:]

    # calculate distances.. each element of this np array is the
    # distance from the point in xy to the next point
    distances = np.sqrt(np.sum(np.square(path[:-1] - path[1:]), axis=1))

    # get a np array of indices where distance are greater than
    # spacing. We'll use this for masking.
    where_to_interp = np.where(distances > spacing)[0]

    # keep track of the offset (for inserting into our output array)
    insert_offset = 0

    # keep track of the indexes to values in xy_out that have been
    # inserted
    inserted_dense_path = []

    for start, end, distance, xy_where in zip(path[where_to_interp],
                                              path[where_to_interp + 1],
                                              distances[where_to_interp],
                                              where_to_interp + 1):
        num_steps = int(distance / spacing + 1)
        interp_points = np.vstack([np.linspace(start[0], end[0], num_steps),
                                   np.linspace(start[1], end[1], num_steps)]).T
        insert_point = xy_where + insert_offset
        dense_path = np.vstack([dense_path[:insert_point], interp_points[1:-1],
                            dense_path[insert_point:]])

        # keep track of the indexes of values that were inserted
        inserted_dense_path.extend(xrange(insert_point, insert_point + len(interp_points) - 2))

        # increment the offset by the amount we just inserted
        insert_offset += len(interp_points[1:-1])

    if values is None:
        return dense_path
    else:
        # indexes of all values in dense_path
        p1 = np.arange(len(dense_path))

        # indexes of values that have not been inserted into dense_path
        p = np.setdiff1d(p1, inserted_dense_path)
        
        # interpolate values values
        interpolated_values = interp1d(p,z)(p1)
        return (xy_out.T[0], xy_out.T[1], interpolated_values)


def interpolate_duplicated_gps(path):
    """
    correct duplicated gps coordinates caused by gps transceiver updates being slower than sounder pings 
    by linear interpolation between successive changed gps coordinates. This function should be run *after* 
    any boat path/gps signal loss corrections. The inherent assumption being that the vehicle speed does not
    change significantly between successive transceiver updates. path is an ordered set of xy points of shape 
    (n, 2)
    """

    x_interp = _interp_between_duplicates(path[:,0])
    y_interp = _interp_between_duplicates(path[:,1])

    return np.vstack((x_interp, y_interp)).T
    

def _interp_between_duplicates(x):  
    """
    replaces an array with duplicate values with new array of same size that replaces the duplicates with 
    linearly interplotated values. i.e
    if 
    x = np.array([1.0,1.0,1.0,2.0,2.0,3.0,3.0,3.0,4.0,4.0,5.0,5.0,5.0,5.0,6.0,6.0])
    then
    interp_between_duplicates(x) = np.array([ 1.        ,  1.33333333,  1.66666667,  2.        ,  2.5       ,
    3.        ,  3.33333333,  3.66666667,  4.        ,  4.5       ,
    5.        ,  5.25      ,  5.5       ,  5.75      ,  6.        ,  6.        ])
    

    OR if
    x = np.array([1.0,1.0,1.0,2.0,2.0,3.0,3.0,3.0,4.0,4.0,2.0,2.0,1.0,1.0,1.0,6.0])
    then                  
    interp_between_duplicates(x) = np.array([ 1.        ,  1.33333333,  1.66666667,  2.        ,  2.5       ,
    3.        ,  3.33333333,  3.66666667,  4.        ,  3.        ,
    2.        ,  1.5       ,  1.        ,  2.66666667,  4.33333333,  6.        ])
    """

    #the next three lines only works for monotonic arrays
    #xUnique, xUniqueIndices = np.unique(x, return_index=True)
    #idx = np.argsort(xUniqueIndices)
    #return np.interp(np.arange(len(x)), xUniqueIndices[idx], xUnique[idx])

    xtmp = x.copy()
    xtmp[1:] = x[1:] - x[:-1]
    x_idx = np.nonzero(xtmp)[0]
    x_vals = x[x_idx]
    return np.interp(np.arange(len(x)),x_idx, x_vals)