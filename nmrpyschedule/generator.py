'''
@author: matt
'''
import itertools
import math



def uniform(ranges):
    '''
    Generate a table of n-dimensional points containing all grid points within the given ranges.
    Includes both boundaries.
    '''
    theNums = [list(range(low, high + 1)) for (low, high) in ranges]
    return itertools.product(*theNums)


_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
def _haltonNumber(index, base):
    result = 0
    f = 1. / base
    i = index
    while i > 0:
        result = result + f * (i % base)
        i = int(i / base)
        f = f / base
    return result

def _scaledHaltonNumber(factor, shift, index, prime):
    return int(factor * _haltonNumber(index, prime)) + shift

def halton(ranges):
    '''
    Generate subrandom sequence of n-dimensional points according to the Halton sequence.
    Returns a generator of an infinite sequence.
    '''
    scalingFactors = [max(x) - min(x) for x in ranges]
    shifts = [min(x) for x in ranges]
    if len(ranges) > len(_primes):
        raise ValueError("not enough primes defined: please define more or reduce the dimensionality")
    ix = 0
    while True:
        pt = []
        for (sf, s, p) in zip(scalingFactors, shifts, _primes):
            pt.append(_scaledHaltonNumber(sf, s, ix, p))
        yield pt
        ix += 1


def _distance(pt, origin):
    zipped = list(zip(pt, origin))
    sumSquares = sum([abs(a - b) ** 2 for (a, b) in zipped])
    dist = math.sqrt(sumSquares)
    return dist

def _myDist(pt, origin, width, maxDeviation):
    dist = _distance(pt, origin)
    ratio = dist / width
    return abs(ratio - round(ratio)) * width <= maxDeviation

def concentricShell(ranges, shellSpacing, maxDeviation):
    '''
    Generate all points whose distance from the origin is close to a multiple
    of an arbitrary number.  The origin is defined as the point whose coordinates
    are the low end of each dimension's range.
    '''
    points = uniform(ranges)
    origin = [r[0] for r in ranges]
    return [pt for pt in points if _myDist(pt, origin, shellSpacing, maxDeviation)]


def _myFilter(pt, origin, offsetAngle, degreeGap, tolerance):
    y,x = pt[0] - origin[0], pt[1] - origin[1]
    theta = m.atan2(x, y) * 180. / m.pi # angle in degrees
    ratio = (theta + offsetAngle) / degreeGap
    return abs(ratio - round(ratio)) * degreeGap < tolerance

def radial(ranges, offsetAngle, gapAngle, maximumDeviation):
    '''
    Generate coordinates of points, where the points lie along 'spokes' radiating out from the origin.
    '''
    allPoints = uniform(ranges)
    origin = [r[0] for r in ranges]
    return [pt for pt in allPoints if _myFilter(pt, origin, offsetAngle, gapAngle, maximumDeviation)]
