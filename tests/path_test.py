import numpy as np
import numpy.testing as npt
from smear.path import _interp_between_duplicates

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