import numpy as np
import numpy.testing as npt
from smear.path import densify_path, interpolate_duplicated_gps, _interp_between_duplicates

def test_densify_path():
    x = np.array([1.,2.,3.,5.,8.,9.,10.])
    y = np.array([1.,2.,3.,5.,8.,9.,10.])

    xi = np.array([1.,2.,3.,4.,5.,6.,7.,8.,9.,10.])
    yi = np.array([1.,2.,3.,4.,5.,6.,7.,8.,9.,10.])

    path = np.vstack((x,y)).T
    pathi = np.vstack((xi,yi)).T
    
    npt.assert_almost_equal(pathi, densify_path(path, 1.4142))


def test_interpolate_duplicated_gps():
    x = np.array([1.0,1.0,1.0,2.0,2.0,3.0,3.0,3.0,4.0,4.0,5.0,5.0,5.0,5.0,6.0,6.0])
    xi = np.array([ 1. ,  1.33333333,  1.66666667,  2.  ,  2.5,
                    3. ,  3.33333333,  3.66666667,  4.  ,  4.5,
                    5. ,  5.25      ,  5.5       ,  5.75,  6. ,  6.])

    y = np.array([1.0,1.0,1.0,2.0,2.0,3.0,3.0,3.0,4.0,4.0,2.0,2.0,1.0,1.0,1.0,6.0])
    yi = np.array([ 1.        ,  1.33333333,  1.66666667,  2.        ,  2.5       ,
                    3.        ,  3.33333333,  3.66666667,  4.        ,  3.        ,
                    2.        ,  1.5       ,  1.        ,  2.66666667,  4.33333333,  6.])

    path = np.vstack((x,y)).T
    pathi = np.vstack((xi,yi)).T

    npt.assert_almost_equal(pathi, interpolate_duplicated_gps(path), verbose=False)


def test_interp_between_duplicates():
    x = np.array([1.0,1.0,1.0,2.0,2.0,3.0,3.0,3.0,4.0,4.0,5.0,5.0,5.0,5.0,6.0,6.0])
    xi = np.array([ 1. ,  1.33333333,  1.66666667,  2.  ,  2.5,
                    3. ,  3.33333333,  3.66666667,  4.  ,  4.5,
                    5. ,  5.25      ,  5.5       ,  5.75,  6. ,  6.])

    npt.assert_almost_equal(_interp_between_duplicates(x), xi) 
    
    x = np.array([1.0,1.0,1.0,2.0,2.0,3.0,3.0,3.0,4.0,4.0,2.0,2.0,1.0,1.0,1.0,6.0])
    xi = np.array([ 1.        ,  1.33333333,  1.66666667,  2.        ,  2.5       ,
                    3.        ,  3.33333333,  3.66666667,  4.        ,  3.        ,
                    2.        ,  1.5       ,  1.        ,  2.66666667,  4.33333333,  6.])

    npt.assert_almost_equal(_interp_between_duplicates(x), xi) 