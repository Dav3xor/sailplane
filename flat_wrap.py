import math
import shapely
from geometry import *
from rivets import *
def split(a,b):
    return a + ((b-a)/2)








def flat_box(coords,shapes,tabs,tx=0,ty=0):
    base = shapes[0]
    flattened = {shapes[0][1]:(distance(coords[shapes[0][0]],
                               coords[shapes[0][1]]),0),
                 shapes[0][0]:(0,0)} 
    cur_perimeter = [flattened[shapes[0][0]],flattened[shapes[0][1]]]
    perimeter = Polygon()
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
    perimeter = Polygon(list(zip(*poly.exterior.coords.xy)))
    perimeter.translate(tx,ty)
                
    #perimeter = [(p[0]+tx,p[1]+ty) for p in perimeter]
    fold_lines = [((l[0][0]+tx,l[0][1]+ty),
                   (l[1][0]+tx,l[1][1]+ty)) for l in fold_lines]
    return perimeter,fold_lines



# this is currently used to place ribs along the wing...
def points_on_a_line(a,b,num_divisions):
    # beware fenceposting, with a num_divisions of 4, you get 3 divisions.
    #
    # this is what makes sense to me
    distance_between = distance(a,b)
    vector = (b[0]-a[0],
              b[1]-a[1],
              b[2]-a[2])
    points = Polygon(closed=False)
    for i in range(1,num_divisions):
        d = (1/(num_divisions))*i
        #print(f'distance a->b {distance(a,b)}')
        #print(f'distance_between {distance_between}')
        #print(f'd a->b {d}')
        #print(f'vector {vector}')
        #print(f'reconstituded b {(a[0]+vector[0],a[1]+vector[1],a[2]+vector[2])}')
        points.append((a[0] + (d*vector[0]),
                     a[1] + (d*vector[1]),
                     a[2] + (d*vector[2])))
    return points 

def load_airfoil(filename):
    coords = []
    with open(filename,'r') as infile:
        for line in infile:
            if line[0].isnumeric():
                x,y = line.split(' ')
                coords.append((float(x), float(y)))
    return coords



def find_airfoil_extents(airfoil,thickness):
    result = []
    for i in reversed(airfoil):
        if i[0] == thickness:
            result.append(i[1])
    return result

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



        
def ellipses(ellipses, hoffset=0, numsteps = 100, flip=False):
    for e in ellipses:
        e['points'] = make_unit_ellipse(e, flip=flip, numsteps=numsteps)
    voffset = 0
    results = []
    for i in range(len(ellipses)-1):
        a = ellipses[i]['points'].copy()
        b = ellipses[i+1]['points'].copy()
        translate_poly(a, ellipses[i]['datum'], ellipses[i]['vertical_center'], ellipses[i]['horizontal_center'])
        translate_poly(b, ellipses[i+1]['datum'], ellipses[i+1]['vertical_center'], ellipses[i+1]['horizontal_center'])

        a1 = (ellipses[i]['datum'], ellipses[i]['skin_split'], ellipses[i]['width'])
        a2 = (ellipses[i]['datum'], ellipses[i]['skin_split'], ellipses[i]['width']*-1)
        b1 = (ellipses[i+1]['datum'], ellipses[i+1]['skin_split'], ellipses[i+1]['width'])
        b2 = (ellipses[i+1]['datum'], ellipses[i+1]['skin_split'], ellipses[i+1]['width']*-1)
        
        if ellipses[i]['skin_split'] and ellipses[i+1]['skin_split']:
            if a1[1] != a[0][1] and b1[1] != b[0][1]:
                a.prepend(a1)
                a.append(a2)
                b.prepend(b1)
                b.append(b2)
                ellipses[i]['flat_ends'] = True
            else:
                ellipses[i]['flat_ends'] = False


        voffset,a_flat,b_flat = build_flat_shape(a,
                                                 b,
                                                 voffset, hoffset)
        # I only have triangles start with one point, going to two, ymmv for other designs --
        if ((not ellipses[i]['skin_split']) or (a1 == a[0])) and (ellipses[i+1]['skin_split']) and (b[0] != b1):
            #print(a[0])
            #print(b[0])
            #print(b1)
            d1 = distance(a[0],b1)
            d2 = distance(b[0],b1)
            p1 = find_pointr(a_flat[0],b_flat[-1],d1,d2)
            p2 = find_pointl(a_flat[-1],b_flat[0],d1,d2)
            b_flat.prepend(p2)
            b_flat.append(p1)
            #b_flat = [p2] + b_flat + [p1]
        print(a_flat+b_flat)
        voffset-=2
        results.append((a_flat,
                        b_flat, 
                        True if ( 'flat_ends' in ellipses[i] and ellipses[i]['flat_ends'] == True) else False))        
    return results


def make_tab(a,b,width=.75,tilt=.2, flip=False):
    base_angle = math.atan2(a[0]-b[0],a[1]-b[1])
    points = Polygon()
    angle = math.atan2(a[0]-b[0], a[1]-b[1])
    if flip:
        angle += 3.14159
        tilt *= -1 
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
        # 8 and .002 work reasonably well.
        #poly = poly.buffer(op,quad_segs=8)
        poly = poly.buffer(op,quad_segs=10)
    poly = shapely.get_parts(poly)[0]
    return Polygon(list(zip(*poly.exterior.coords.xy)))

def fancy_notch(angle, center, length, spread):
    points = []
    points.append(center)
    points.append((center[0]+(math.sin(angle-spread)*length),
                  center[1]+(math.cos(angle-spread)*length)))
    points.append((center[0]+(math.sin(angle+spread)*length),
                  center[1]+(math.cos(angle+spread)*length)))
    
    return round_corners(points,.15)

# subtract b from a
def difference(a,b):
    pa = shapely.Polygon(a)
    pb = shapely.Polygon(b)
    pc = shapely.difference(pa,pb,grid_size=.01)
    pc = shapely.get_parts(pc)[0]
    return Polygon(list(zip(*pc.exterior.coords.xy)))

def simplify(a):
    pa = shapely.Polygon(a)
    #pa = shapely.simplify(pa,.002)
    pa = shapely.simplify(pa,.005)
    pa = shapely.get_parts(pa)[0]
    return Polygon(list(zip(*pa.exterior.coords.xy)))



def make_notched_bulkhead(points, split, notches,tx,ty, side='bottom'):
    def place_notch(p1,p2):
        angle = math.atan2(points[p1][0]-points[p2][0], 
                           points[p1][1]-points[p2][1])+(math.pi/2)
        if side == 'bottom':
            setback_point = (points[p1][0]+(math.sin(angle-math.pi)*.25),
                             points[p1][1]+(math.cos(angle-math.pi)*.25))
            notch1 = fancy_notch(math.atan2(points[p1][0]-points[p2][0], 
                                            points[p1][1]-points[p2][1]) + (math.pi/2),
                                 setback_point,2,.15)
        else:
            setback_point = (points[p1][0]-(math.sin(angle-math.pi)*.25),
                             points[p1][1]-(math.cos(angle-math.pi)*.25))
            notch1 = fancy_notch(math.atan2(points[p1][0]-points[p2][0], 
                                            points[p1][1]-points[p2][1]) - (math.pi/2),
                                 setback_point,2,.15)
        notch2 = [(i[0]*-1,i[1]) for i in notch1]
        return notch1,notch2

    # (outside) sheet metal cutout, including flanges/notches
    bulkhead_shape = simplify(round_corners(points, .75))

    #print(round_corners(points, .75).translate(tx,ty))
   
    
    skip = notches[0] if len(notches) > 0 else 0
    # remove the bottom/top corners
    if side == 'bottom':
        left_corner  = ((points[0][0]*-1.0-1, split-.375),
                        (points[0][0]*-1.0-1, split+1),
                        (points[0][0]*-1.0+.375, split+1),
                        (points[0][0]*-1.0+.25, split-.25))
    else:
        left_corner  = ((points[0][0]*-1.0-1, split+.375),
                        (points[0][0]*-1.0-1, split-1),
                        (points[0][0]*-1.0+.375, split-1),
                        (points[0][0]*-1.0+.25, split+.25))
    
    # copy/mirror the left bottom corner 
    right_corner = [(i[0]*-1,i[1]) for i in left_corner]

    #print(round_corners(left_corner,.25).translate(tx,ty))
    #print(round_corners(right_corner,.25).translate(tx,ty))
    left_corner  = round_corners(left_corner,.25)
    right_corner = round_corners(right_corner,.25)
  
    top_notch = fancy_notch(math.pi*-1,(points[200][0],points[200][1]+.25),2,.25)
    #print(top_notch.translate(tx,ty))
    bulkhead_shape = difference(bulkhead_shape,top_notch)
    bulkhead_shape = difference(bulkhead_shape,left_corner)
    bulkhead_shape = difference(bulkhead_shape,right_corner)

    #print(top_notch.translate(tx,ty))

    prev_p   = skip
    cur_p    = 0
    next_end = 0




    notch1,notch2  = place_notch(cur_p,cur_p+1)
    bulkhead_shape = difference(bulkhead_shape,notch1)
    bulkhead_shape = difference(bulkhead_shape,notch2)

    #while next_end != None and cur_p+next_end < len(points)//2-10:
    for notch_distance in notches[1:]:
        next_end = polyline_point_after_distance(points[cur_p:len(points)//2],notch_distance)[0]
        cur_p = prev_p + next_end 

        notch1,notch2 = place_notch(cur_p-1,cur_p)

        holes_on_a_line(points[prev_p:cur_p], .6, .3,tx,ty)

        bulkhead_shape = difference(bulkhead_shape,notch1)
        bulkhead_shape = difference(bulkhead_shape,notch2)
        
        
        prev_p = cur_p



    print(simplify(round_corners(bulkhead_shape,-.05,.1,-.05)).translate(tx,ty))
    print(bulkhead_shape.color('red').translate(tx,ty))


def connecting_strip(centerline, edges, width, skip, tx=0,ty=0, flat_ends=False):
    a = []
    b = []
    if flat_ends:
        start = 2
        end = len(centerline)-2
        a+=(make_tab(centerline[0],centerline[1], tilt=.4, flip=True))
    else:
        start = 1
        end = len(centerline)-1
        a.append(centerline[0])

    # ...
    for i in range(start, end):
        p1 = centerline[i]
        p2 = centerline[i+1]
        angle = math.atan2(p1[0]-p2[0], p1[1]-p2[1])
        if i % skip:
            a.append((p1[0]+width*math.sin(angle+(math.pi/2)),
                      p1[1]+width*math.cos(angle+(math.pi/2))))
        else:
            a.append((p1[0]+(width/10)*math.sin(angle-(math.pi/2)),
                      p1[1]+(width/10)*math.cos(angle-(math.pi/2))))
    if flat_ends:
        a+=(make_tab(centerline[-2],centerline[-1], tilt=.4, flip=True))
    else:
        a.append(centerline[-1])

    p1 = centerline[0]
    p2 = centerline[1]
    angle = math.atan2(p1[0]-p2[0], p1[1]-p2[1])
    b.append((p1[0]+width*math.sin(angle-(math.pi/2)-.2),
              p1[1]+width*math.cos(angle-(math.pi/2)-.2)))
          
    for i in range(1,len(centerline)-2):
        p1 = centerline[i]
        p2 = centerline[i+1]
        angle = math.atan2(p1[0]-p2[0], p1[1]-p2[1])
        b.append((p1[0]+width*math.sin(angle-(math.pi/2)),
                  p1[1]+width*math.cos(angle-(math.pi/2))))
    
    p1 = centerline[-1]
    p2 = centerline[-2]
    angle = math.atan2(p1[0]-p2[0], p1[1]-p2[1])
    b.append((p1[0]+width*math.sin(angle+(math.pi/2)+.2),
              p1[1]+width*math.cos(angle+(math.pi/2)+.2)))


    
    b.reverse()

    print(Polygon(a+b).translate(tx,ty))




def expand_airfoil(airfoil,chord,datum, sweep):
    points = Polygon(closed=False)
    for i in range(len(airfoil)):
        points.append(((airfoil[i][0]*chord)+sweep,
                       airfoil[i][1]*chord,
                       datum))
    return points



# location is 'top' 'bottom' or 'both'
# TODO: properly handle location when applicable
def insert_airfoil_point(airfoil, percent_chord, location='both'):
    locations, index, existed = find_airfoil_location(airfoil, percent_chord)
    # if the points are not currently in the airfoil, add them
    if not existed[0]:
        airfoil.insert(index[0],locations[0])
    if not existed[1]:
        airfoil.insert(index[1],locations[1])
    return locations, index, existed

# cuts the trailing end off
def trim_airfoil(airfoil, percent_chord, location='both'):
    trimmed = airfoil.copy()
    locations, index, existed = insert_airfoil_point(trimmed,percent_chord, location)
    if index:
        if location in ['top','both']:
            trimmed = trimmed[index[0]:]
        if location in ['bottom','both']:
            trimmed = trimmed[:index[1]]
    return trimmed

# returns the trailing end
def trim_airfoil_end(airfoil, percent_chord):
    locations, index, existed = insert_airfoil_point(airfoil,percent_chord, 'both')
    if index:
        top    = airfoil[:index[0]]
        bottom = airfoil[index[1]:] 
        # TODO: 
    return top,bottom


def find_airfoil_location(airfoil, percent_chord):
    def find(airfoil, percent_chord):
        prev = airfoil[0]
        for i in range(len(airfoil[1:])):
            next = airfoil[i]
            if prev[0] == percent_chord:
                return prev, i, True # True = there was already a point at that percent_chord
            elif (prev[0] > percent_chord) and next[0] < percent_chord:
                #print(f'prev={prev} next={next}')
                slope = (next[1]-prev[1])/(next[0]-prev[0])
                #print(slope)
                y = slope*(percent_chord-prev[0])+prev[1]
                result = ((percent_chord,y))
                #print(result)
                return result, i, False   # False = it did not exist
            else:
                prev = next
        return None, None, None
    a, ba, aexisted = find(airfoil, percent_chord)
    reversed = airfoil.copy()
    reversed.reverse()
    b, bb, bexisted = find(reversed, percent_chord)
    return(a,b),(ba,-1*bb),(aexisted,bexisted)

def wing_skin(shapes1, chord1, shapes2, chord2, span, sweep, num_ribs=None, tx=0, ty=0,aft_cut=None, spanlines=[[]]):
    for i in range(len(shapes1)):
        airfoil1 = shapes1[i].copy()
        airfoil2 = shapes2[i].copy()
        if i==0:
            for location in spanlines[i]:
                insert_airfoil_point(airfoil1, location)
                insert_airfoil_point(airfoil2, location)
        af1_shape = expand_airfoil(airfoil1, chord1, 0, 0)
        af2_shape = expand_airfoil(airfoil2, chord2, span, sweep)
      
        
        print(af1_shape.translate(tx,ty-20))
        print(af2_shape.translate(tx,ty-20))

        af1_shape.translate(tx*-1,(ty-20)*-1)
        af2_shape.translate(tx*-1,(ty-20)*-1)

        if num_ribs != None: 
            ribs = [Polygon() for j in range(num_ribs)]
            for j in range(len(af1_shape)):
                points = points_on_a_line(af1_shape[j],af2_shape[j],num_ribs)
                for k in range(len(points)):
                    ribs[k].append(points[k])
            for rib in ribs:
                print(rib.translate(tx,ty-20))


        a,b,c = build_flat_shape(af1_shape, af2_shape, voffset=ty, hoffset=tx-(i*30))
        print(b+c)
        for line in spanlines[i]:
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
    spar = Polygon([(chord_a*extents_a[1][1], 0),
            (chord_a*extents_a[0][1], 0),
            (chord_b*extents_b[0][1], span),
            (chord_b*extents_b[1][1], span)])
    print(spar.translate(tx,ty))
   

# this keeps the first two points, and triangulates the third, returns
# svg (I need to change this)
def flat_triangle(pa,pb,d1,d2,side='left'):
    poly = Polygon()
    poly.append(pa)
    poly.append(pb)
    pc = find_pointl(pa,pb,d1,d2) if side == 'left' else find_pointr(pa,pb,d1,d2)
    poly.append(pc)
    return poly

def build_dashed_line(a,b):
    return f'<line stroke-width="0.1" stroke="blue" stroke-dasharray="0.5, 0.5" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"></line>'

def build_flat_fan(pivot, fan, start_pivot=(0,0), start_point=None, reverse=False, tx=0,ty=0,direction='left', color='black'):
    flattened = Polygon(color=color)
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
    flattened.translate(tx,ty)
    print(flattened)
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

        new_a = find_pointl(flattened_a[-1], flattened_b[-1], d1, slant1)
        new_b = find_pointl(new_a, flattened_a[-1], base2, slant2)
        
        flattened_a.append(new_a)
        flattened_b.append(new_b)

    points = ''

    # all the points are in order in the svg, so you have to 
    # reverse the b side, otherwise it would skip back to the 
    # beginning.
    flattened_b.reverse()
    
    #print((flattened_a+flattened_b).translate(tx,ty))
   


    #return ((height*-1.0)+voffset, 
    #        [(i[0]+tx,i[1]+ty) for i in flattened_a], 
    #        [(i[0]+tx,i[1]+ty) for i in flattened_b])
    flattened_a = Polygon(flattened_a)
    flattened_b = Polygon(flattened_b)
    flattened_a.translate(tx,ty)
    flattened_b.translate(tx,ty)
    return  ((height*-1.0)+voffset, flattened_a, flattened_b)
    #return (height*-1.0)+voffset


