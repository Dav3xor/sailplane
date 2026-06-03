import shapely
from geometry import *

# code for rivets and tabs



# finds a point at distance
# from point a towards point b (2d)
def point_on_a_line(a,b,length):
    distance_between = distance(a,b)
    vector = ((b[0]-a[0])/distance_between,
              (b[1]-a[1])/distance_between)
    return (a[0] + (length*vector[0]),
            a[1] + (length*vector[1]))

def point_along_polyline(line,distance):
    stuff = polyline_point_after_distance(line,distance)
    if stuff:
        p2, cur_distance = stuff
        #print(stuff)
        #print("+")
        p1 = p2-1
        #print(f'{p1} - {p2} {distance} {cur_distance}')
        return (p1,p2,point_on_a_line(line[p1],line[p2],cur_distance))
    else:
        #print("-")
        return None

def points_along_polyline(line,start_margin,num_points, offset=.75, end_margin=None, side='bottom'):
    points = []

    if not end_margin:
        end_margin = start_margin

    def position_point(p):
        p1,p2,p = p
        if side=='bottom':
            angle = math.atan2(line[p1][0]-line[p2][0], 
                               line[p1][1]-line[p2][1])+(math.tau/4)
        else:
            angle = math.atan2(line[p1][0]-line[p2][0], 
                               line[p1][1]-line[p2][1])-(math.tau/4)
        op = (p[0]+math.sin(angle)*offset, 
              p[1]+math.cos(angle)*offset)
        points.append(op)

    total_length     = polyline_distance(line)
    available_length = total_length-(start_margin+end_margin)
    
    if num_points == 1:
        segment_length = available_length/2
        p = point_along_polyline(line,start_margin+segment_length)
        if p:
            position_point(p)
    else:
        cur_pos          = start_margin
        segment_length   = available_length/(num_points-1)
        for point in range(num_points):
            p = point_along_polyline(line,cur_pos)
            if p:
                position_point(p)
                cur_pos    += segment_length
    return points

def polyline_point_after_distance(line,total_length):
    #print(line)
    if len(line) < 2:
        #print('a')
        return 0
    else:
        length = 0
        for i in range(len(line)-1):
            cur_len = distance(line[i],line[i+1])
            if length+cur_len > total_length:
                #print(f'b{i}')
                #TODO problem seems to be here
                return i+1, total_length-length#-cur_len
            length+=cur_len
        #print('c')
        return None

def polyline_distance(line):
    print(line)
    if len(line) < 2:
        return 0
    else:
        length = 0
        for i in range(len(line)-1):
            length += distance(line[i],line[i+1])
        print(length)
        return length




# well, not really a line, more like holes on a polyline (typically an arc)
def holes_on_a_line(line, start_margin, min_distance,tx,ty,side='bottom', end_margin=None):
    if not end_margin:
        end_margin = start_margin
    # rivet hole spacing
    rline = line.copy()
    rline.reverse()
    #print("x")
    arc_distance = polyline_distance(line)
    if arc_distance:
        available_arc = arc_distance-(start_margin+end_margin)
        num_holes = math.ceil(available_arc/min_distance)
        points = points_along_polyline(line,start_margin,num_holes,offset=.375,side=side, end_margin=end_margin)
        
        for point in points:
            circle = shapely.Point(point).buffer(.125)
            circle = Polygon(list(zip(*circle.exterior.coords.xy)))
            print(circle.translate(tx,ty))
    #print(f'distance = {arc_distance} available_arc = {available_arc} num_holes = {num_holes}')
        
