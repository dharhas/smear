from timeit import Timer
import numpy as np

setup_base = "import numpy as np; from scipy.interpolate import griddata; \
		from smear.interpolate import Interpolator; points = np.random.random((%r,2)); \
		values = np.random.random(%r); xi = np.random.random((%r,2))"


results = []

for n in 10**(np.arange(2,6)):
	print n
	setup = setup_base % (n, n, 10)
	t1 = Timer("griddata(points, values, xi, method='linear')", setup).timeit(100)
	t2 = Timer("Interpolator(points, values)(xi, method='linear', nnear=10)", setup).timeit(100)
	results.append([n, t1, t2])

linear_scale_points = np.array(results)
np.save('linear_scale_points', linear_scale_points)

results = []

for n in 10**(np.arange(1,6)):
	print n
	setup = setup_base % (100000, 100000, n)
	t1 = Timer("griddata(points, values, xi, method='linear')", setup).timeit(100)
	t2 = Timer("Interpolator(points, values)(xi, method='linear', nnear=10)", setup).timeit(100)
	results.append([n, t1, t2])

linear_scale_target = np.array(results)
np.save('linear_target_points', linear_scale_target)

for n in 10**(np.arange(2,6)):
	print n
	setup = setup_base % (n, n, 10)
	t1 = Timer("griddata(points, values, xi, method='cubic')", setup).timeit(100)
	t2 = Timer("Interpolator(points, values)(xi, method='cubic', nnear=100)", setup).timeit(100)
	results.append([n, t1, t2])

cubic_scale_points = np.array(results)
np.save('cubic_scale_points', cubic_scale_points)

results = []

for n in 10**(np.arange(1,6)):
	print n
	setup = setup_base % (100000, 100000, n)
	t1 = Timer("griddata(points, values, xi, method='cubic')", setup).timeit(100)
	t2 = Timer("Interpolator(points, values)(xi, method='cubic', nnear=100)", setup).timeit(100)
	results.append([n, t1, t2])

cubic_scale_target = np.array(results)
np.save('cubic_target_points', cubic_scale_target)