import math



def get_intersections(p1, r1, p2, r2):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d=math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
    
    # non intersecting
    if d > r1 + r2 :
        print("non intersecting")
        return None
    # One circle within other
    if d < abs(r1-r2):
        print("within")
        return None
    # coincident circles
    if d == 0 and r1 == r2:
        print("coincident")
        return None
    else:
        a=(r1**2-r2**2+d**2)/(2*d)
        h=math.sqrt(r1**2-a**2)

        p3 = ( p1[0]+a*(p2[0]-p1[0])/d,
               p1[1]+a*(p2[1]-p1[1])/d )

        p4 = ( p3[0]+h*(p2[1]-p1[1])/d,
               p3[1]-h*(p2[0]-p1[0])/d )

        p5 = ( p3[0]-h*(p2[1]-p1[1])/d,
               p3[1]+h*(p2[0]-p1[0])/d )
        return (p4,p5)

def isleft(a, b, c):
  return (b[0] - a[0])*(c[1] - a[1]) - (b[1] - a[1])*(c[0] - a[0]) > 0;
  return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x) > 0;

def find_pointl(a,b,A,B):
    points = get_intersections(a,A,b,B)
    if points:
        return points[0] if isleft(a,b,points[0]) else points[1]
    else:
        print("?")
        exit(0)

def find_pointr(a,b,A,B):
    points = get_intersections(a,A,b,B)
    if points:
        return points[1] if isleft(a,b,points[0]) else points[0]
    else:
        print("?")
        exit(0)



def distance(a,b):
    if len(a) == 3:
        return distance3(a[0]-b[0], a[1]-b[1],a[2]-b[2])
    if len(a) == 2:
        return distance2(a[0]-b[0], a[1]-b[1])
def distance3(dx,dy,dz):
    return math.sqrt(dx**2 + dy**2 + dz**2)

def distance2(dx,dy):
    return math.sqrt(dx**2 + dy**2)


def tri_anglea(a,b,c):
  stuff = ((b**2)+(c**2)-(a**2)) / (2*b*c)
  print(f'anglea {stuff}')
  return math.acos( stuff )

def tri_angleb(a,b,c):
  stuff = ((a**2)+(c**2)-(b**2)) / (2*a*c)
  print(f'angleb {stuff}')
  return math.acos(stuff)

def load_airfoil(filename):
    coords = []
    with open(filename,'r') as infile:
        for line in infile:
            if line[0].isnumeric():
                x,y = line.split(' ')
                coords.append((float(x), float(y)))
    return coords


# assumes A is at (0,0) and B is on the X axis
# you will have to rotate this into position
def pointc(AB,BC,AC):
    x = (AB**2 + AC**2 - BC**2)/(2*AB)
    y = math.sqrt(abs(AC**2 - x**2))
    return (x,y)

def rotate(point, angle):
    return (point[0]*math.cos(angle) - point[1]*math.sin(angle),
            point[0]*math.sin(angle) + point[1]*math.cos(angle))

print('<svg viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">')


def make_ellipse(e, numsteps = 100, flip=False):
    points = []
    flip = -1.0 if flip else 1.0
    for step in range(numsteps):
        step_angle = (2*3.14159*e['amount'])/(numsteps-1)
        angle = step * step_angle
        points.append(( (math.cos(angle)*e['width'])+e['horizontal_center'], 
                        (math.sin(angle)*e['height']*flip)+e['vertical_center'],
                        e['datum']))
    return points

def ellipses(ellipses):
    for e in ellipses:
        e['points'] = make_ellipse(e)
    voffset = 0
    for i in range(len(ellipses)-1):
        voffset = build_flat_shape(ellipses[i]['points'],
                                    ellipses[i+1]['points'], 
                                    voffset)


def expand_airfoil(airfoil,chord,datum, sweep):
    points = []
    for i in range(len(airfoil)):
        points.append(((airfoil[i][0]*chord)+sweep,
                       airfoil[i][1]*chord,
                       datum))
    return points


def points_to_poly(points):
    poly = ''
    for point in points:
        poly += f'{point[0]},{point[1]} \n'

    return f'<polygon stroke-width="0.1" fill="none" stroke="black" points="{poly}" />'

def wing_skin(airfoil1, chord1, airfoil2, chord2, span, sweep):
    build_flat_shape(expand_airfoil(airfoil1, chord1, 0, 0),
                     expand_airfoil(airfoil2, chord2, span, sweep))

def wing_rib(airfoil, chord):
    print(points_to_poly(expand_airfoil(airfoil,chord,0,0)))


def build_flat_shape(a,b, voffset=0):
    print(a)
    print(b)
    flattened_a  = []
    flattened_b  = []
   
    
    height = distance(a[0],b[0])
    
    flattened_a.append((0,voffset))
    flattened_b.append((0,(height*-1.0)+voffset))



    for step in range(1, len(a)):
        # get side lengths on the original shape in 3d
        d1 = distance(a[step],a[step-1])
        d2 = distance(b[step],b[step-1])

        slant1 = distance(b[step-1],a[step])
        slant2 = distance(a[step-1],b[step])

        #print(f'd1{d1} d2{d2} slant1{slant1} slant2{slant2} a{flattened_a[-1]} b{flattened_b[-1]}')
        new_a = find_pointl(flattened_a[-1], flattened_b[-1], d1, slant1)
        new_b = find_pointr(flattened_b[-1], flattened_a[-1], d2, slant2)
        
        flattened_a.append(new_a)
        flattened_b.append(new_b)


    points = ''

    # all the points are in order in the svg, so you have to 
    # reverse the b side, otherwise it would skip back to the 
    # beginning.
    flattened_b.reverse()

    print(points_to_poly(flattened_a+flattened_b))

    return (height*-1.0)+voffset


