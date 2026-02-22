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

def points_along_polyline(line,margin,num_points, offset=.75):
    total_length     = polyline_distance(line)
    cur_pos          = margin
    available_length = total_length-(margin*2)
    segment_length   = available_length/(num_points-1)
    points = []
    for point in range(num_points):
        p = point_along_polyline(line,cur_pos)
        if p:
            p1,p2,p = p
            cur_pos    += segment_length
            angle = math.atan2(line[p1][0]-line[p2][0], line[p1][1]-line[p2][1])+(math.tau/4)
            op = (p[0]+math.sin(angle)*offset, 
                  p[1]+math.cos(angle)*offset)
            points.append(op)
    return points

# this is the old function, TODO: remove
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
    if len(line) < 2:
        return 0
    else:
        length = 0
        for i in range(len(line)-1):
            length += distance(line[i],line[i+1])
        return length




# TODO: deprecated, remove...
# well, not really a line, more like holes on a polyline (typically an arc)
def holes_on_a_line(line, end_margin, min_distance,tx,ty):
    # rivet hole spacing
    rline = line.copy()
    rline.reverse()
    arc_distance = polyline_distance(line)
    if arc_distance:
        available_arc = arc_distance-(end_margin*2)
        num_holes = math.floor(available_arc/min_distance)
        if num_holes < 1:
            num_holes = 1
        distance_between_holes = available_arc/(num_holes+1)
        holes = []
        if num_holes == 1:
            holes.append(line[polyline_point_after_distance(line, arc_distance/2)[0]])
        if num_holes == 2:
            holes.append(line[polyline_point_after_distance(line, end_margin)[0]])
            holes.append(rline[polyline_point_after_distance(rline, end_margin)[0]])
            #holes.append(end_margin)
            #holes.append(arc_distance-end_margin)
        if num_holes == 3:
            holes.append(line[polyline_point_after_distance(line, end_margin)[0]])
            holes.append(rline[polyline_point_after_distance(rline, end_margin)[0]])
            holes.append(line[polyline_point_after_distance(line, arc_distance/2)[0]])

            #holes.append(end_margin)
            #holes.append(end_margin+(available_arc/2))
            #holes.append(arc_distance-end_margin)

        for hole in holes:
            print(hole)
            # TODO: find position on line
            circle = shapely.Point(hole).buffer(.125)
            points = list(zip(*circle.exterior.coords.xy))
            print(points_to_poly(points, tx=tx, ty=ty))
        print(f'distance = {arc_distance} available_arc = {available_arc} num_holes = {num_holes} holes = {holes}')
        
