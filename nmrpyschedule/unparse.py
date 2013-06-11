import json



def bruker(points):
    raise ValueError('unimplemented')


def _wagnerPoint(point):
    chunks = []
    for coordinate in point:
        chunks.extend([str(coordinate), '\n'])
    return ''.join(chunks)
    

def wagner(points):
    '''
    input:
      - a point is an iterable of integers
    
    output:
      - one time delay per line.  A single two-dimensional point spans two lines, 
        a three-dimensional point spans three lines
      - no quadrature support
      - one-indexed:  the coordinates of the 'first' point are ones
      - ordered by time delays
      - naturally supports non-uniform transients:  just add points multiple times to the input
        
    example (two-dimensional):
    1
    1
    3
    5
    
    The first point is (1,1), the second is (3,5), etc.
    '''
    formattedPoints = map(_brukerPoint, sorted(points))
    return ''.join(formattedPoints)


def _toolkitPoint(point, quads):
    chunks = []
    for c in point:
        chunks.extend([str(c), ' '])
    if len(quads) == 0:
        raise ValueError(('unable to toolkit-format grid point with no quadrature components', point))
    for q in sorted(quads):
        chunks.extend([q, ' '])
    chunks.append('\n')
    return chunks


def toolkit(points):
    '''
    input:
      - a point is a pair of 1) iterable of integers, 2) quadrature component
    
    output:
      - one grid point per line, including all (>= 1) quadrature components
      - one-indexed:  the time delays of the 'first' point are ones
      - ordered by time delays
      - quadrature components sorted lexicographically
      - non-uniform transients:  not supported
    
    example (two-dimensional):
    1 1 II IR RI RR
    3 5 II
    3 50 II IR RI RR
    5 9 IR RI RR
    8 19 II RR
    8 65 II IR RI RR
    9 35 RR
    15 1 IR RR
    
    The first point is (1,1) with all four quadrature components.
    '''
    # 1. group points by time increments
    groupedPoints = {}
    for (delays, quad) in points:
        key, quadKey = tuple(delays), tuple(quad)
        if not groupedPoints.has_key(key):
            groupedPoints[key] = set([])
        quads = groupedPoints[key]
        if quadKey in quads:
            raise ValueError(('duplicate transient in toolkit formatting', (delays, quad)))
        quads.add(quadKey)
    # 2. sort by time increments
    sortedPoints = sort(groupedPoints, key=lambda (ts,_): ts)
    
    chunks = []
    # 3. sort quadrature components
    # 4. format points
    for (ts, qs) in sortedPoints:
        chunks.extend(_toolkitPoints(ts, qs))
    return ''.join(chunks)
    

def toolkitNoQuadrature(points):
    '''
    input:
      - a point is an iterable of integers

    output:
      - one point per line
      - one-indexed
      - no quadrature support
      - ordered by time delays
      - no support for non-uniform transients
      
    example:
    1 1
    3 5
    3 50
    5 9
    '''
    raise ValueError('not implemented')


def _vqPoint(ts, quad):
    chunks = []
    for t in ts:
        chunks.extend([str(t - 1), ' '])
    chunks.append(quad)
    return ''.join(chunks)
    
    
def varianQuadrature(points):
    '''
    input:
      - a point is a pair of 1) iterable of integers, 2) quadrature component
    
    output:
      - one point per line
      - zero-indexed
      - ordered by time delays, then quadrature component
      - non-uniform transients simply by repeating points
        
    example (two-dimensional):
    0 0 II
    0 0 IR
    0 0 RI
    0 0 RR
    2 4 II
    2 4 RR
    2 49 RR
    '''
    sortedPoints = sort(points) # um, does this sort right?
    return '\n'.join(map(_vqPoint, sortedPoints))


def asJSON(points):
    '''
    input:
      - a point is a pair of 1) iterable of integers, 2) quadrature component
    
    output:
      - one-indexed
      - JSON-formatted text string
    
    example:
    [{'times': [1, 2], 'quad': 'RR'}, {'times': [1,2], 'quad': 'RI'}, ... etc. ...]
    '''
    jsonPoints = []
    for (ts, q) in points:
        jsonPoints.append({'times': ts, 'quad': q})
    return json.dumps(jsonPoints)
