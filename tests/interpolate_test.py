import numpy as np
import numpy.testing as npt
from scipy.interpolate import griddata
from smear.interpolate import Interpolator

def test_nearest():
	points = np.random.random((100,2))
	values = np.random.random(100)
	xi = np.random.random((10,2))

	vi_target = griddata(points, values, xi, method='nearest')

	vi = Interpolator(points, values)(xi, method='nearest')

	npt.assert_array_equal(vi, vi_target)

def test_cubic():
	points = np.random.random((100,2))*100
	values = np.random.random(100)*100
	xi = np.random.random((10,2))

	vi_target = griddata(points, values, xi, method='cubic')

	vi = Interpolator(points, values)(xi, method='cubic', nnear=100)
	npt.assert_almost_equal(vi, vi_target)

	vi = Interpolator(points, values)(xi, method='cubic', nnear=10)
	npt.assert_almost_equal(vi, vi_target)

def test_linear():
	points = np.random.random((100,2))*100
	values = np.random.random(100)*100
	xi = np.random.random((10,2))*50

	vi_target = griddata(points, values, xi, method='linear')

	vi = Interpolator(points, values)(xi, method='linear', nnear=100)
	npt.assert_almost_equal(vi, vi_target)

	vi = Interpolator(points, values)(xi, method='linear', nnear=10)
	npt.assert_almost_equal(vi, vi_target)

def test_idw():
	pass
