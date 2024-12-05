import math
import shapely


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

print('<svg width="200in" height="200in" viewBox="0 0 200 200" viewboxxmlns="http://www.w3.org/2000/svg">')


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

def ellipses(ellipses, hoffset=0):
    for e in ellipses:
        e['points'] = make_ellipse(e)
    voffset = 0
    results = []
    for i in range(len(ellipses)-1):
        voffset,a,b = build_flat_shape(ellipses[i]['points'],
                                       ellipses[i+1]['points'], 
                                       voffset, hoffset)
        voffset-=2
        results.append((a,b))        
    
    return results

def connecting_strip(centerline, edges, width, skip):
    a = []
    b = []
    
    a.append(centerline[0])
    
    for i in range(1, len(centerline)-1):
        p1 = centerline[i]
        p2 = centerline[i+1]
        angle = math.atan2(p1[0]-p2[0], p1[1]-p2[1])
        if i % skip:
            a.append((p1[0]+width*math.sin(angle+(math.pi/2)),
                      p1[1]+width*math.cos(angle+(math.pi/2))))
        else:
            a.append((p1[0]+(width/10)*math.sin(angle-(math.pi/2)),
                      p1[1]+(width/10)*math.cos(angle-(math.pi/2))))
        b.append((p1[0]+width*math.sin(angle-(math.pi/2)),
                  p1[1]+width*math.cos(angle-(math.pi/2))))
    a.append(centerline[-1])
    b.reverse()
    poly = shapely.Polygon(a+b)
    #poly = poly.buffer(.05, cap_style=3).buffer(-.05, join_style=1)
    #poly = poly.buffer(-0.1).buffer(.2).buffer(-0.1)
    poly = poly.buffer(-.1)
    poly2 = '' 
    for point in list(zip(*poly.exterior.coords.xy)):
        poly2 += f'{point[0]},{point[1]} \n'
    print (f'<polygon stroke-width="0.1" fill="none" stroke="black" points="{poly2}" />')
    for edge in edges:
        points = []
        poly = ''
        angle = math.atan2(edge[0][0]-edge[1][0], edge[0][1]-edge[1][1])
        points.append((edge[0][0]+width*math.sin(angle+(math.pi/2)),
                  edge[0][1]+width*math.cos(angle+(math.pi/2))))
        points.append((edge[0][0]+width*math.sin(angle-(math.pi/2)),
                  edge[0][1]+width*math.cos(angle-(math.pi/2))))
        points.append((edge[1][0]+width*math.sin(angle-(math.pi/2)),
                  edge[1][1]+width*math.cos(angle-(math.pi/2))))
        points.append((edge[1][0]+width*math.sin(angle+(math.pi/2)),
                  edge[1][1]+width*math.cos(angle+(math.pi/2))))
        for point in points:
            poly += f'{point[0]},{point[1]} \n'
        print (f'<polygon stroke-width="0.1" fill="none" stroke="black" points="{poly}" />')
        


    return a+b
        



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
    af1_shape = expand_airfoil(airfoil1, chord1, 0, 0)
    af2_shape = expand_airfoil(airfoil2, chord2, span, sweep)
   
    print(points_to_poly(af1_shape))
    print(points_to_poly(af2_shape))
    a,b,c = build_flat_shape(af1_shape, af2_shape)
    connecting_strip(c,[],.75,3)
    # I used this to determine which parts of the 
    #print(af1_shape[50:90])
    return (af1_shape, af2_shape,a)

def wing_rib(airfoil, chord):
    print(points_to_poly(expand_airfoil(airfoil,chord,0,0)))

def flat_triangle(pa,pb,d1,d2,side='left'):
    poly = ''
    poly += f'{pa[0]},{pa[1]} \n'
    poly += f'{pb[0]},{pb[1]} \n'
    pc = find_pointl(pa,pb,d1,d2) if side == 'left' else find_pointr(pa,pb,d1,d2)
    poly += f'{pc[0]},{pc[1]} \n'
    return f'<polygon stroke-width="0.1" fill="none" stroke="black" points="{poly}" />'

def build_flat_fan(pivot, fan):
    flattened = []
    
    height = distance(pivot,fan[0])
    flattened.append((0, height))
    print(height)
    print(flattened)
    for step in range(1,len(fan)):
        d     = distance(fan[step],fan[step-1])
        slant = distance(pivot,fan[step])
        print(f"---\n{flattened}")
        print(f'd={d} slant={slant} step={step} base = {distance((0,0),flattened[-1])}')
        # -- flatspace

        newp = find_pointl((0,0), flattened[-1],slant,d)
        flattened.append(newp)
    flattened.append((0,0))
    print(points_to_poly(flattened))
    
def build_flat_shape(a,b, voffset=0, hoffset=0):
    #print(a)
    #print(b)
    flattened_a  = []
    flattened_b  = []
   
    
    height = distance(a[0],b[0])
    
    flattened_a.append((0+hoffset,voffset))
    flattened_b.append((0+hoffset,(height*-1.0)+voffset))



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
    
    return ((height*-1.0)+voffset, flattened_a, flattened_b)
    #return (height*-1.0)+voffset


