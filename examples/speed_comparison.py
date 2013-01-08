from timeit import Timer
import numpy as np



#setup = "import pandas; male_trips=pandas.load('maletrips')"
#a  = "male_trips.start_station_id.value_counts()"
#b = "male_trips.groupby('start_station_id').size()"
#Timer(a,setup).timeit(100)
#Timer(b,setup).timeit(100)

setup_base = "import numpy as np; from scipy.interpolate import griddata; \
		from smear.interpolate import Interpolator; points = np.random.random((%r,2)); \
		values = np.random.random(%r); xi = np.random.random((%r,2))"

setup = setup_base % (100,100, 10)
t1 = Timer("griddata(points, values, xi, method='cubic')", setup).timeit(100)
t2 = Timer("Interpolator(points, values)(xi, method='cubic', nnear=100)", setup).timeit(100)

print t1, t2