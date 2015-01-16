__author__ = 'pawel'


TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)

X = 0
Y = 1


def turn(p, q, r):
    # Cross-product
    return cmp((q[X] - p[X])*(r[Y] - p[Y]) - (r[X] - p[X])*(q[Y] - p[Y]), 0)


def _keep_left(hull, r):
    while len(hull) > 1 and turn(hull[-2], hull[-1], r) != TURN_LEFT:
        hull.pop()
    # Handle degenerate cases (ie. multisets)
    if not hull or hull[-1] != r:
        hull.append(r)
    return hull


def convex_hull(points):
    """Returns points on convex hull of an array of points in CCW order."""
    points = sorted(points)
    l = reduce(_keep_left, points, [])
    u = reduce(_keep_left, reversed(points), [])
    # We don't include the first or last point when extending l.
    l.extend(u[i] for i in xrange(1, len(u) - 1))
    return l

