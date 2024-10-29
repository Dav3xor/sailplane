import math


cones = [{'height': 6, 'base_radius': 10, 'top_radius': 8, 'amount': 0.5},
        {'height': 6, 'base_radius': 11.5, 'top_radius': 10, 'amount': 0.5},
        {'height': 6, 'base_radius': 12.5, 'top_radius': 11.5, 'amount': 0.5},
        {'height': 9.5, 'base_radius': 13.5, 'top_radius': 12.5, 'amount': 0.5},
        {'height': 8.5, 'base_radius': 14, 'top_radius': 13.5, 'amount': 0.5}]

#ellipses = [
#        #{'height': 36, 'tx': 12, 'ty': 9, 'bx': 6, 'by': 4.5, 'amount': 0.5},
#        #{'height': 7*12, 'tx': 6, 'ty': 4.5, 'bx': 2, 'by': 1.5, 'amount': 0.5},
#        {'height': 10, 'tx':9, 'ty':9, 'bx':10, 'by':8, 'amount': 1.0},
#        {'height': 10, 'tx': 10, 'ty': 8, 'bx': 5, 'by': 5, 'amount': 1.0},
#        {'height': 10, 'tx': 5, 'ty': 5, 'bx': 6, 'by': 6, 'amount': 1.0}
#        ]

fuselage = [
        {'vertical_center': 0, 'horizontal_center': 0, 'width':1, 'height':1, 'datum':0, 'amount': 1.0},
        {'vertical_center': 0, 'horizontal_center': 0, 'width':5, 'height':5, 'datum':5, 'amount': 1.0},
        {'vertical_center': 0, 'horizontal_center': 0, 'width':6, 'height':6, 'datum':10, 'amount': 1.0}
        ]


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

center = 0
def cones(cones):
    for cone in cones:
        base_width   = cone['base_radius'] * 2.0
        top_width    = cone['top_radius'] * 2.0
        cone_height  = (cone['height'] * base_width) / (base_width-top_width)

        band_width   = distance2((cone['base_radius']-cone['top_radius']), cone['height'])
        outer_radius = distance2(cone_height, cone['base_radius'])

        inner_radius = outer_radius - band_width
        angle = (360.0 * ((3.14159*base_width)/(3.14159*2*outer_radius))) * cone['amount']
        rad_angle = (angle*3.14159)/180.0
        
        print('<circle cx="{}" cy="0" r="{}" fill="none" stroke="black" />'.format(center, outer_radius))
        print('<circle cx="{}" cy="0" r="{}" fill="none" stroke="black" />'.format(center, inner_radius))
        print('<polyline points="{},{} {},{} {},{}" fill="none" stroke="black" />'.format(
            center+outer_radius+5, 0,
            center, 0,
            center+(math.cos(rad_angle)*(outer_radius+5)), 
                    math.sin(rad_angle)*(outer_radius+5) ))
        center += 200 

numsteps = 100


def ellipses(ellipses):
    for e in ellipses:
        e['points'] = []
        for step in range(numsteps):
            step_angle = (2*3.14159*e['amount'])/numsteps
            angle = step * step_angle
            e['points'].append(( (math.cos(angle)*e['width'])+e['horizontal_center'], 
                                 (math.sin(angle)*e['height'])+e['vertical_center'],
                                e['datum']))
    for i in range(len(ellipses)-1):
        build_flat_shape(ellipses[i]['points'],ellipses[i+1]['points'])


def expand_airfoil(airfoil,chord,datum, sweep):
    points = []
    for i in range(len(airfoil)):
        points.append(((airfoil[i][0]*chord)+sweep,
                       airfoil[i][1]*chord,
                       datum))
    return points

def wing_skin(airfoil1, chord1, airfoil2, chord2, span, sweep):
    build_flat_shape(expand_airfoil(airfoil1, chord1, 0, 0),
                     expand_airfoil(airfoil2, chord2, span, sweep))
        


def build_flat_shape(a,b):
    print(a)
    print(b)
    flattened_a  = []
    flattened_b  = []
   
    
    height = distance(a[0],b[0])
    
    flattened_a.append((0,0))
    flattened_b.append((0,height*-1.0))



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

    for point in flattened_a:
        points += '{},{} \n'.format(point[0],point[1])

    # all the points are in order in the svg, so you have to 
    # reverse the b side, otherwise it would skip back to the 
    # beginning.
    flattened_b.reverse()
    for point in flattened_b:
        points += '{},{} \n'.format(point[0],point[1])

    print('<polygon stroke-width="0.1" fill="none" stroke="black" points="{}" />'.format(points))

def build_flat_shape_old(top,bottom):
    flattened_top  = []
    flattened_bottom  = []
    
    dx = top[0][0] - bottom[0][0]
    dy = top[0][1] - bottom[0][1]
    dz = top[0][2] - bottom[0][2]
    
    height = distance3(dx,dy,dz)

    flattened_top.append((0,0))
    flattened_bottom.append((0,height*-1.0))



    for step in range(1, len(top)):
        dx = abs(top[step][0]     - bottom[step][0])
        dy = abs(top[step][1]     - bottom[step][1])
        dz = abs(top[step][2]     - bottom[step][2])
        
        height = distance3(dx,dy,dz)

        top_len = distance3(top[step-1][0]-top[step][0],
                            top[step-1][1]-top[step][1],
                            top[step-1][2]-top[step][2])

        bottom_len = distance3(bottom[step-1][0]-bottom[step][0],
                               bottom[step-1][1]-bottom[step][1],
                               bottom[step-1][2]-bottom[step][2])
        

        angle = math.atan2(flattened_top[-1][1] - flattened_bottom[-1][1],
                           flattened_top[-1][0] - flattened_bottom[-1][0])-(3.14159/2.0)

        topx = flattened_top[-1][0] + (math.cos(angle)*top_len)
        topy = flattened_top[-1][1] + (math.sin(angle)*top_len)

        angle2 = math.atan2(flattened_bottom[-1][1]-topy,
                            flattened_bottom[-1][0]-topx)
        
        AB = distance2(topx-flattened_bottom[-1][0],
                       topy-flattened_bottom[-1][1])
        
        flattened_top.append((topx,topy))
       
        hyp = pointc(AB,bottom_len,height)
        #print("pre {}".format(hyp))
        bp  = rotate(hyp, angle2)
        #print("before {}".format(bp))
        bp = (bp[0] + topx, bp[1] + topy)
        #print("after {}".format(bp))
        flattened_bottom.append(bp)


        #print('tx {} ty {}'.format(topx, topy))
        #print('bx {} by {}'.format(flattened_bottom[-1][0],
        #                           flattened_bottom[-1][1]))

    points = ''

    for point in flattened_top:
        points += '{},{} \n'.format(point[0],point[1])

    flattened_bottom.reverse()
    for point in flattened_bottom:
        points += '{},{} \n'.format(point[0],point[1])

    print('<polygon stroke-width="0.1" fill="none" stroke="black" points="{}" />'.format(points))


ellipses(fuselage)
airfoil1 = load_airfoil('GA40-A620.dat')
airfoil2 = load_airfoil('GA40-A610.dat')
wing_skin(airfoil1, 48, airfoil2, 20, 36,30)

print('</svg>')    



