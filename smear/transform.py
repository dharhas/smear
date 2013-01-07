import numpy as np
from pyproj import Proj
import requests
from shapely.geometry import LineString, Point


def projection(srs_code):
    return Proj(retrieve_projection_params(srs_code))


def retrieve_projection_params(srs_code, format='proj4'):
    #http://spatialreference.org/ref/esri/102737/proj4/

    base_url = 'http://spatialreference.org/ref/'
    tags = srs_code.lower().strip().split(':') + [format.strip() + '/']
    url = base_url + '/'.join(tags)
    r = requests.get(url)

    if r.status_code == 200:
        return r.text
    else:
        raise ValueError('Unable to retrieve projection details for %s in format %s from \
            spatialreference.org, error message received: %s - %s' % (srs_code, format, r.status_code, r.reason))


class SN_CoordinateSystem:
    """ 
    Define an SN Coordinate System based on a given centerline
    Convert xy dataset into sn Coordinate System based on a given centerline.
    """

    def __init__(self, cx, cy, slope_distance=0.01, interp=None, interp_params=[]):
        """
        Initialize SN coordinate system. Requires arrays containing cartesian x,y values 
        and arrays containing centerline cx,cy cartesian coordinates 
        """

        if interp is not None:
            cx, cy = self.smooth_centerline(cx, cy, interp, interp_params) 

        self.centerline = LineString(zip(cx.tolist(), cy.tolist()))
        self.slope_distance = slope_distance

    def norm(self, x):
        return np.sqrt(np.square(x).sum())

    def smooth_centerline(self, x, y, interp, interp_params):
        #todo add other interp types like bezier curves

        #spline:

        #spline parameters
        s=3.0 # smoothness parameter
        k=2 # spline order
        nest=-1 # estimate of number of knots needed (-1 = maximal)
        xnew = np.array([])
        ynew = np.array([])

        for start, end, spacing in interp_params:
            if spacing==-1:
                xtmp = x[start:end]
                ytmp = y[start:end]
            else:
                npts = int(LineString(zip(x[start:end].tolist(), y[start:end].tolist())).length / spacing) 
                # find the knot points
                tckp,u = splprep([x[start:end],y[start:end]],s=s,k=k,nest=-1)
                xtmp, ytmp = splev(np.linspace(0,1,npts),tckp)

            xnew = np.concatenate((xnew,xtmp))
            ynew = np.concatenate((ynew,ytmp))

        return (xnew, ynew)
                         
    def transform_xy_to_sn(self, x, y):
        s = np.zeros(x.size)
        n = np.zeros(x.size)
        v = np.zeros((x.size,2))
        vn = np.zeros((x.size,2))
        for ii in range(x.size):
            pt = Point((x[ii],y[ii]))
            s[ii] = self.centerline.project(pt)
            pt_s = self.centerline.interpolate(s[ii])
            pt_s1 = self.centerline.interpolate(s[ii] - self.slope_distance)
            pt_s2 = self.centerline.interpolate(s[ii] + self.slope_distance)
            vn[ii,0] = pt.x - pt_s.x
            vn[ii,1] = pt.y - pt_s.y
            v[ii,0] = pt_s2.x - pt_s1.x
            v[ii,1] = pt_s2.y - pt_s1.y
            n[ii] = pt_s.distance(pt)

        n = -np.sign(np.cross(v,vn)) * n
        return (s,n)

    def transform_sn_to_xy(self,s,n):
        x = np.zeros(s.size)
        y = np.zeros(s.size)
        unit_normal = np.zeros(2)
        xy = np.zeros(2)
        for ii in range(s.size):
            pt_s = self.centerline.interpolate(s[ii])
            xy[0] = pt_s.x
            xy[1] = pt_s.y
            pt_s1 = self.centerline.interpolate(s[ii] - self.slope_distance)
            pt_s2 = self.centerline.interpolate(s[ii] + self.slope_distance)
            unit_normal[0] = -(pt_s2.y - pt_s1.y)
            unit_normal[1] = (pt_s2.x - pt_s1.x)
            unit_normal = unit_normal/self.norm(unit_normal)
            x[ii], y[ii] = xy - unit_normal*n[ii]
            #theta = np.arctan((pt_s2.x - pt_s1.x)/(pt_s2.y - pt_s1.y))
            #x[ii] = pt_s.x - n[ii]*np.cos(theta)
            #y[ii] = pt_s.y + n[ii]*np.sin(theta)
            
        return (x,y)
