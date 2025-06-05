import math
import shapely


def flat_box(coords,shapes,tabs,tx=0,ty=0):
    base = shapes[0]
    flattened = {shapes[0][1]:(distance(coords[shapes[0][0]],
                               coords[shapes[0][1]]),0),
                 shapes[0][0]:(0,0)} 
    cur_perimeter = [flattened[shapes[0][0]],flattened[shapes[0][1]]]
    perimeter = []
    fold_lines = []
    for shape in shapes:
        print(shape)
        for i in range(len(shape)-2):
            i0 = shape[i]
            i1 = shape[(i+1)%len(shape)]
            i2 = shape[(i+2)%len(shape)]
            
            flattened_a = flattened[i0]
            flattened_b = flattened[i1]
            d1 = distance(coords[i0],
                          coords[i2])
            d2 = distance(coords[i1],
                          coords[i2])
            new_p = find_pointl(flattened_a, flattened_b, d1, d2)
            flattened[i2] = new_p
            cur_perimeter.append(new_p)
        if len(perimeter) == 0:
            perimeter = cur_perimeter
        else:
            print(f'{shape[0]} - {shape[1]}')
            fold_lines.append((flattened[shape[0]],flattened[shape[1]]))
            pos = perimeter.index(flattened[shape[0]])
            #cur_perimeter.reverse()
            perimeter[pos:pos] = cur_perimeter
        cur_perimeter = []
    #print(f'perimeter={perimeter}')
    #5/0
    poly = shapely.Polygon(perimeter)
    for line in fold_lines:
        circle = shapely.Point(*line[0]).buffer(.2)
        #poly = shapely.difference(poly,circle)
        
        circle = shapely.Point(*line[1]).buffer(.2)
        #poly = shapely.difference(poly,circle)
    #poly = poly.buffer(.1)
    #poly = poly.buffer(-.2)
    #poly = poly.buffer(.1)
    perimeter = list(zip(*poly.exterior.coords.xy))
    perimeter = [(p[0]+tx,p[1]+ty) for p in perimeter]
    fold_lines = [((l[0][0]+tx,l[0][1]+ty),
                   (l[1][0]+tx,l[1][1]+ty)) for l in fold_lines]
    return perimeter,fold_lines

# trilateration:
# https://github.com/noomrevlis/trilateration/blob/master/trilateration2D.py
def get_intersections(p1, r1, p2, r2):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    #d=math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
    d = distance(p2,p1)

    # non intersecting
    if d > r1 + r2 :
        print("non intersecting")
        return None
    # One circle within other
    if d < abs(r1-r2):
        print(f"within d={d} r1={r1} r2={r2}")
        return None
    # coincident circles
    if d == 0 and r1 == r2:
        print("coincident")
        return None
    else:
        a = (pow(r1, 2) - pow(r2, 2) + pow(d, 2)) / (2*d)
        h  = math.sqrt(pow(r1, 2) - pow(a, 2))
        x0 = p1[0] + a*(p2[0] - p1[0])/d 
        y0 = p1[1] + a*(p2[1] - p1[1])/d
        rx = -(p2[1] - p1[1]) * (h/d)
        ry = -(p2[0] - p1[0]) * (h / d)
        return ((x0+rx, y0-ry), (x0-rx, y0+ry))

def isleft(a, b, c):
  return (b[0] - a[0])*(c[1] - a[1]) - (b[1] - a[1])*(c[0] - a[0]) > 0;
  return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x) > 0;

def find_pointl(a,b,A,B):
    points = get_intersections(a,A,b,B)
    if points:
        return points[0] if isleft(a,b,points[0]) else points[1]
    else:
        print("?")
        5/0

def find_pointr(a,b,A,B):
    points = get_intersections(a,A,b,B)
    if points:
        return points[1] if isleft(a,b,points[0]) else points[0]
    else:
        print("?")
        5/0



def distance(a,b):
    if len(a) != len(b):
        5/0
    if len(a) == 3:
        return distance3(a[0]-b[0], a[1]-b[1],a[2]-b[2])
    if len(a) == 2:
        return distance2(a[0]-b[0], a[1]-b[1])
def distance3(dx,dy,dz):
    return math.sqrt(dx**2 + dy**2 + dz**2)

def distance2(dx,dy):
    return math.sqrt(dx**2 + dy**2)



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




def quarter_round(radius,zangle=0):
    a = []
    for i in range(10):
        angle = (90/10*i)*2*3.14159/360
        x=0
        y=math.cos(angle)*radius
        z=math.sin(angle)*radius
        a.append((x,y,z))
    return a
def rotatez(points, angle):
    rotated = []
    for point in points:
        newpoint = (point[0]*math.cos(angle) - point[1]*math.sin(angle),
                    point[0]*math.sin(angle) + point[1]*math.cos(angle),
                    point[2])
        rotated.append(newpoint)     
    return rotated
def ellipse_point(angle, e):
    x = math.sin(angle)*e['height']
    y = math.cos(angle)*e['width']
    return 0,x,y

def make_unit_ellipse(e, numsteps = 100, flip=False, mode=1):
    points = []
    flip = -1.0 if flip else 1.0
    for step in range(numsteps):
        step_angle = (2*3.14159*e['amount'])/(numsteps-1)
        angle = step * step_angle
        #if mode == 1:
        #    points.append(( e['datum'],
        #                    (math.sin(angle)*e['height']*flip)+e['vertical_center'],
        #                    (math.cos(angle)*e['width'])+e['horizontal_center']))
        #if mode == 2:
        #    points.append(( (math.sin(angle)*e['height']*flip) + e['datum'],
        #                    e['vertical_center'],
        #                    (math.cos(angle)*e['width']) + e['horizontal_center']))
        if mode == 1:
            points.append(( 0,
                            (math.sin(angle)*e['height']*flip),
                            (math.cos(angle)*e['width'])))
        if mode == 2:
            points.append(( (math.sin(angle)*e['height']*flip),
                            0,
                            (math.cos(angle)*e['width'])))

    return points

def make_ellipse(e, numsteps=100, flip=False, mode=1):
    ellipse = make_unit_ellipse(e,numsteps,flip,mode)
    translate_poly(ellipse, e['datum'], e['vertical_center'], e['horizontal_center'])
    return ellipse

def translate_poly(p, x, y, z):
    for i in range(len(p)):
        p[i] = (p[i][0]+x, 
                p[i][1]+y, 
                p[i][2]+z)

def adjust_ellipse(a,b_old,ea,eb, numsteps=100):
    step_angle = (2*3.14159*ea['amount'])/(numsteps-1)
    b = b_old.copy()
    cur_angles = [i*step_angle for i in range(len(a))]
    for j in range(20):
        #print('---')
        for i in range(len(a)):
            aa = math.atan2(a[i][2], a[i][1])
            ab = math.atan2(b[i][2],b[i][1])
            
            difference = (aa-ab)
            if abs(difference) > .0001:
                cur_angles[i] = cur_angles[i] - (difference / 1.2)
                b[i] = ellipse_point(cur_angles[i],eb)
            #print(f'aa={aa} ab={ab} aa-ab={aa-ab}')
    
    print(points_to_poly(b_old,xindex=1,yindex=2, color="blue"))
    print(points_to_poly(a,xindex=1,yindex=2, color="red"))
    print(points_to_poly(b,xindex=1,yindex=2, color="green"))
    return b
        
def ellipses(ellipses, hoffset=0, numsteps = 100, flip=False):
    for e in ellipses:
        e['points'] = make_unit_ellipse(e, flip=flip, numsteps=numsteps)
    voffset = 0
    results = []
    for i in range(len(ellipses)-1):
        a = ellipses[i]['points'].copy()
        b = ellipses[i+1]['points'].copy()
        #a = adjust_ellipse(b,a,ellipses[i+1],ellipses[i],numsteps=numsteps)
        #b = adjust_ellipse(a,b,ellipses[i],ellipses[i+1],numsteps=numsteps)
        translate_poly(a, ellipses[i]['datum'], ellipses[i]['vertical_center'], ellipses[i]['horizontal_center'])
        translate_poly(b, ellipses[i+1]['datum'], ellipses[i+1]['vertical_center'], ellipses[i+1]['horizontal_center'])
        #print("+++")
        #print(a)
        #print(b)
        #print("+++")
        voffset,a,b = build_flat_shape(a,
                                       b,
                                       voffset, hoffset)
        voffset-=2
        results.append((a,b))        
    return results

def make_tab(a,b,width=.75,tilt=.2):
    base_angle = math.atan2(a[0]-b[0],a[1]-b[1])
    points = []
    angle = math.atan2(a[0]-b[0], a[1]-b[1])
    points.append(a)
    points.append((a[0]+width*math.sin(angle-tilt-(math.pi/2)),
              a[1]+width*math.cos(angle-tilt-(math.pi/2))))
    points.append((b[0]+width*math.sin(angle+tilt-(math.pi/2)),
              b[1]+width*math.cos(angle+tilt-(math.pi/2))))
    points.append(b)
    return points 

def round_corners(points, *ops):
    poly = shapely.Polygon(points)
    #poly = poly.buffer(.05, cap_style=3).buffer(-.05, join_style=1)
    #poly = poly.buffer(-0.1).buffer(.2).buffer(-0.1)
    for op in ops:
        poly = poly.buffer(op)
    return list(zip(*poly.exterior.coords.xy))



def connecting_strip(centerline, edges, width, skip, tx=0,ty=0):
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
    points = list(zip(*poly.exterior.coords.xy))
    print(points_to_poly(points, tx=tx,ty=ty))
    
    for edge in edges:
        points = []
        poly = ''
        angle = math.atan2(edge[0][0]-edge[1][0], edge[0][1]-edge[1][1])
        points.append((edge[0][0]+width*math.sin(angle+(math.pi/2))+tx,
                  edge[0][1]+width*math.cos(angle+(math.pi/2))+ty))
        points.append((edge[0][0]+width*math.sin(angle-(math.pi/2))+tx,
                  edge[0][1]+width*math.cos(angle-(math.pi/2))+ty))
        points.append((edge[1][0]+width*math.sin(angle-(math.pi/2))+tx,
                  edge[1][1]+width*math.cos(angle-(math.pi/2))+ty))
        points.append((edge[1][0]+width*math.sin(angle+(math.pi/2))+tx,
                  edge[1][1]+width*math.cos(angle+(math.pi/2))+ty))
        print(points_to_poly(points, tx=0,ty=0))
        


    return a+b
        



def expand_airfoil(airfoil,chord,datum, sweep):
    points = []
    for i in range(len(airfoil)):
        points.append(((airfoil[i][0]*chord)+sweep,
                       airfoil[i][1]*chord,
                       datum))
    return points


def points_to_poly(points,xindex=0,yindex=1,tx=0.0,ty=0.0, color='black'):
    poly = ''
    for point in points:
        try:
            poly += f'{point[xindex]+tx},{point[yindex]+ty} \n'
        except:
            print(points)
            5/0

    return f'<polygon stroke-width="0.1" fill="none" stroke="{color}" points="{poly}" />'

def points_to_line(p1,p2):
    return f'<line x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}" style="stroke:black;stroke-width:0.1" />'

def wing_skin(airfoil1, chord1, airfoil2, chord2, span, sweep, tx=0, ty=0,spanlines=[]):
    af1_shape = expand_airfoil(airfoil1, chord1, 0, 0)
    af2_shape = expand_airfoil(airfoil2, chord2, span, sweep)
   
    print(points_to_poly(af1_shape,tx=tx,ty=ty-20))
    print(points_to_poly(af2_shape,tx=tx,ty=ty-10))

    a,b,c = build_flat_shape(af1_shape, af2_shape, voffset=ty, hoffset=tx)

    for line in spanlines:
        for i in range(len(airfoil1)):
            if line == airfoil1[i][0]:
                #print(f'{i} - {airfoil1[i]}')
                #print(f'{b[i]},{c[i]}')
                print(points_to_line(b[i],c[-1*i - 1]))

    #connecting_strip(c,[],.75,3)
    # I used this to determine which parts of the 
    #print(af1_shape[50:90])
    return (af1_shape, af2_shape,a)

def wing_spar(chord_a,chord_b,span,extents_a, extents_b,tx=0,ty=0):
    spar = [(chord_a*extents_a[1], 0),
            (chord_a*extents_a[0], 0),
            (chord_b*extents_b[0], span),
            (chord_b*extents_b[1], span)]
    print(points_to_poly(spar, tx=tx, ty=ty))
    
    spar = [(chord_a*extents_a[1]-.125, 0),
            (chord_a*extents_a[0]+.125, 0),
            (chord_b*extents_b[0]+.125, span),
            (chord_b*extents_b[1]-.125, span)]
    print(points_to_poly(spar, tx=tx+10, ty=ty))
            


def wing_rib(airfoil, chord):
    print(points_to_poly(expand_airfoil(airfoil,chord,0,0)))

# this keeps the first two points, and triangulates the third, returns
# svg (I need to change this)
def flat_triangle(pa,pb,d1,d2,side='left'):
    poly = []
    poly.append(pa)
    poly.append(pb)
    pc = find_pointl(pa,pb,d1,d2) if side == 'left' else find_pointr(pa,pb,d1,d2)
    poly.append(pc)
    return poly

def build_dashed_line(a,b):
    return f'<line stroke-width="0.1" stroke="blue" stroke-dasharray="0.5, 0.5" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"></line>'

def build_flat_fan(pivot, fan, start_pivot=(0,0), start_point=None, reverse=False, tx=0,ty=0,direction='left'):
    flattened = []
    if reverse:
        fan.reverse()
    if not start_point:
        height = distance(pivot,fan[0])
        flattened.append((0, height))
    else:
        flattened.append(start_point)
    for step in range(1,len(fan)):
        d     = distance(fan[step],fan[step-1])
        slant = distance(pivot,fan[step])
        #print(f"---\n{flattened}")
        #print(f'd={d} slant={slant} step={step} base = {distance((0,0),flattened[-1])}')
        # -- flatspace

        if direction == 'left':
            newp = find_pointl(start_pivot, flattened[-1],slant,d)
        else:
            newp = find_pointr(start_pivot, flattened[-1],slant,d)

        flattened.append(newp)
    flattened.append(start_pivot)
    print(points_to_poly(flattened,tx=tx,ty=ty))
    return flattened

#takes a triangle in any orientation in 3d, makes a 2d flattened equivalent.  I hope.
def build_2d_triangle(a,b,c):
    a2 = (0,0)
    b2 = (0,distance(a,b))
    c2 = find_pointl(a2,b2,distance(a,c),distance(b,c))
    return (a2,b2,c2)

# builds a flat shape from 2 lists of points -- fuselage skin sections, wing
# skin sections, etc...
def build_flat_shape(a,b, voffset=0, hoffset=0, start=None, tx=0, ty=0):
    #print(a)
    #print(b)
    flattened_a  = []
    flattened_b  = []
   
    height = distance(a[0],b[0])
   
    if start:
        flattened_a.append(start[-1])
        flattened_b.append(start[-2])
    else:
        
        flattened_a.append((0+hoffset,voffset))
        flattened_b.append((0+hoffset,(height*-1.0)+voffset))



    for step in range(1, len(a)):
        # get side lengths on the original shape in 3d
        d1 = distance(a[step],a[step-1])
        d2 = distance(b[step],b[step-1])

        base1  = distance(a[step-1],b[step-1])
        base2  = distance(a[step],b[step])

        slant1 = distance(b[step-1],a[step])
        slant2 = distance(a[step-1],b[step])

        #print(f'd1{d1} d2{d2} slant1{slant1} slant2{slant2} a{flattened_a[-1]} b{flattened_b[-1]}')
        #new_a = find_pointl(flattened_a[-1], flattened_b[-1], d1, slant1)
        #new_b = find_pointr(flattened_b[-1], flattened_a[-1], d2, slant2)
        #new_a = find_pointl(flattened_b[-1], flattened_a[-1], slant1, d1)
        new_a = find_pointl(flattened_a[-1], flattened_b[-1], d1, slant1)
        new_b = find_pointl(new_a, flattened_a[-1], base2, slant2)
        #new_b = find_pointl(new_a, flattened_b[-1], slant1, d2)
        #new_b = find_pointl(new_a, flattened_b[-1], base2, d2)
        
        flattened_a.append(new_a)
        flattened_b.append(new_b)

    points = ''

    # all the points are in order in the svg, so you have to 
    # reverse the b side, otherwise it would skip back to the 
    # beginning.
    flattened_b.reverse()
    
    print(points_to_poly(flattened_a+flattened_b, tx=tx, ty=ty))
    
    return ((height*-1.0)+voffset, flattened_a, flattened_b)
    #return (height*-1.0)+voffset


