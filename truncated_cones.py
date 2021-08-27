import math


cones = [{'height': 6, 'base_radius': 10, 'top_radius': 8, 'amount': 0.5},
        {'height': 6, 'base_radius': 11.5, 'top_radius': 10, 'amount': 0.5},
        {'height': 6, 'base_radius': 12.5, 'top_radius': 11.5, 'amount': 0.5},
        {'height': 9.5, 'base_radius': 13.5, 'top_radius': 12.5, 'amount': 0.5},
        {'height': 8.5, 'base_radius': 14, 'top_radius': 13.5, 'amount': 0.5}]

ellipses = [
        #{'height': 36, 'tx': 12, 'ty': 9, 'bx': 6, 'by': 4.5, 'amount': 0.5},
        #{'height': 7*12, 'tx': 6, 'ty': 4.5, 'bx': 2, 'by': 1.5, 'amount': 0.5},
        {'height': 10, 'tx':9, 'ty':9, 'bx':10, 'by':8, 'amount': 1.0},
        {'height': 10, 'tx': 10, 'ty': 8, 'bx': 5, 'by': 5, 'amount': 1.0},
        {'height': 10, 'tx': 5, 'ty': 5, 'bx': 6, 'by': 6, 'amount': 1.0}
        ]

def distance3(dx,dy,dz):
    return math.sqrt(dx**2 + dy**2 + dz**2)

def distance2(dx,dy):
    return math.sqrt(dx**2 + dy**2)


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

for e in ellipses:
    top        = []
    bottom     = []
    flattened_top  = []
    flattened_bottom  = []
    step_angle = (2*3.14159*e['amount'])/numsteps

    for step in range(numsteps):
        angle = step * step_angle
        top.append((math.cos(angle)*e['tx'], 
                    math.sin(angle)*e['ty']))
        bottom.append((math.cos(angle)*e['bx'], 
                       math.sin(angle)*e['by']))
        #print("{} {} - {} {}".format(step,angle,top[step],bottom[step]))
    
    dx = top[0][0] - bottom[0][0]
    dy = top[0][1] - bottom[0][1]
    dz = e['height']
    height = distance3(dx,dy,dz)

    flattened_top.append((0,0))
    flattened_bottom.append((0,height*-1.0))



    for step in range(1, numsteps):
        dx = abs(top[step][0] - bottom[step][0])
        dy = abs(top[step][1] - bottom[step][1])
        dz = e['height']
        height = distance3(dx,dy,dz)

        top_len = distance2(top[step-1][0]-top[step][0],
                            top[step-1][1]-top[step][1])

        bottom_len = distance2(bottom[step-1][0]-bottom[step][0],
                               bottom[step-1][1]-bottom[step][1])
        #print("tl {} bl {}".format(top_len, bottom_len))

        angle = math.atan2(flattened_top[-1][1] - flattened_bottom[-1][1],
                           flattened_top[-1][0] - flattened_bottom[-1][0])-(3.14159/2.0)

        topx = flattened_top[-1][0] + (math.cos(angle)*top_len)
        topy = flattened_top[-1][1] + (math.sin(angle)*top_len)

        angle2 = math.atan2(flattened_bottom[-1][1]-topy,
                            flattened_bottom[-1][0]-topx)
        #print(angle2)
        AB = distance2(topx-flattened_bottom[-1][0],
                       topy-flattened_bottom[-1][1])
        #print("{} {}".format(AB,height))
        flattened_top.append((topx,topy))
        #print("lengths {} {} {}",AB,bottom_len,height)
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

    print('<polyline fill="none" stroke="black" points="{}" />'.format(points))

print('</svg>')    
