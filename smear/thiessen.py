"""
module for computing thiessen polygons
"""
import numpy as np
from scipy.spatial import Delaunay


def thiessen(points, bounds_scale=5):
    """Return list of thiessen polygons for given 2d numpy array of
    points. ``bounds_scale`` is basically a measure of how far out the
    bounding thiessen polygons will be created. If it's too large, set
    it smaller; if it's too small make it bigger. For most
    applications, you'll want to clip the polygons yourself at some
    point so making them too big isn't a problem.
    """
    # something that is way bigger than the points
    x_scale, y_scale = (points.min(axis=0) - points.max(axis=0)) * bounds_scale

    means = np.ones((4, 2)) * points.mean(axis=0)

    scale_offsets = np.array([
        [-1 * x_scale, -1 * y_scale],
        [-1 * x_scale,  y_scale],
        [x_scale, -1 * y_scale],
        [x_scale,  y_scale]])

    outer_box = means + scale_offsets

    points = np.vstack([points, outer_box])
    tri = Delaunay(points)
    circumcenters = np.array([_circumcenter(tri.points[t])
                              for t in tri.vertices])
    thiessen_polys = [_thiessen_poly(tri, circumcenters, n)
                      for n in range(len(points) - 4)]

    return thiessen_polys


def plot_thiessen(points, bounds_scale=10):
    """quick plot of thiessen polygons for a given set of point"""
    from matplotlib import pyplot as plt
    polys = thiessen(points, bounds_scale)
    plt.scatter(points[:, 0], points[:, 1])
    for poly in polys:
        poly = np.vstack([poly, poly[0]])
        plt.plot(poly[:, 0], poly[:, 1], 'r')
        poly = np.vstack([poly, poly[0]])
    plt.show()


#---------------------------------------------------------------------------
# internal functions
#---------------------------------------------------------------------------
def _any_equal(arr, n):
    """for a given Mx3 array, returns a 1xM array containing indices
    of rows where any of the columns are equal to n.
    """
    return np.where((arr[:, 0] == n) | (arr[:, 1] == n) | (arr[:, 2] == n))[0]


def _circumcenter(vertices):
    """returns the circumcenter of a triangle.

    ``vertices`` should be a np.array of size (3,2) containing the
    points of the triangle
    """
    ax, ay, bx, by, cx, cy = vertices.flatten()

    D = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))

    # don't divide by 0
    if D == 0:
        D = 0.000000001

    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / D
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / D

    return ux, uy


def _find_triangles_for_vertex(tri, n):
    """returns all of the indices of the triangles for the nth vertex
    of a given a scipy.spatial.Delaunay object
    """
    # grab the list of triangles that touch this vertex
    triangles = tri.vertices[_any_equal(tri.vertices, n)]

    # we want to sort the triangles so that neighbors are together,
    # just start with the first triangle
    sorted_triangles = [triangles[0]]

    # initialize values
    if triangles[0][0] != n:
        previous_vertex_idx = triangles[0][0]
    else:
        previous_vertex_idx = triangles[0][1]

    # just stash the common vertex for checking if we're sorted
    # clockwise later on
    common_edge_vertex_idx = previous_vertex_idx

    # loop through the triangles; previous_vertex_index will be the
    # index to the vertex we used in the previous triangle
    for i in triangles[1:]:
        this_triangle = sorted_triangles[-1]

        # find the vertex of the triangle that is not the central
        # vertex and is not shared with the previous triangle
        next_vertex_idx = this_triangle[(this_triangle != n) & (this_triangle != previous_vertex_idx)]

        # append the next triangle (note: match will return both the
        # previous triangle and the next triangle, since they both
        # contain the shared vertex)
        matching_triangles = triangles[_any_equal(triangles, next_vertex_idx)]
        if np.all(this_triangle == matching_triangles[0]):
            sorted_triangles.append(matching_triangles[1])
        else:
            sorted_triangles.append(matching_triangles[0])

        previous_vertex_idx = next_vertex_idx

    sorted_triangle_indices = [
        int(np.where(np.all(tri.vertices[:] == triangle, axis=1))[0])
        for triangle in sorted_triangles]

    # if we're sorted counter-clockwise, then we need to reverse order
    test_point = tri.points[triangles[0][(triangles[0] != n) & (triangles[0] != common_edge_vertex_idx)]].flatten()
    if not _is_right(tri.points[n], tri.points[common_edge_vertex_idx], test_point):
        return sorted_triangle_indices[::-1]

    # otherwise we're good
    return sorted_triangle_indices


def _is_right(a, b, p):
    """given a line (defined by points a and b) and a point (p),
    return true if p is to the right of the line and false otherwise

    raises a ValueError if p lies is colinear with a and b
    """
    ax, ay = a[0], a[1]
    bx, by = b[0], b[1]
    px, py = p[0], p[1]
    value = (bx - ax) * (py - ay) - (by - ay) * (px - ax)

    if value == 0:
        raise ValueError(
            "p is colinear with a and b, 'tis neither right nor left.")

    return value < 0


def _thiessen_poly(tri, circumcenters, n):
    """given a Delaunay triangulation object, calculates a thiessen
    polygon for the vertex index n
    """
    triangles = _find_triangles_for_vertex(tri, n)
    triangles = np.hstack((triangles, triangles[0]))
    return [circumcenters[t] for t in triangles]
