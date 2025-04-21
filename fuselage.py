import math 
from flat_wrap import * # general dimensions:
import numpy as np
import matplotlib.pyplot as plt

flange_width          = .75
seat_width            = 19
seat_half_width       = seat_width/2.0
console_height        = 14

#console / seat bottom coordinates
seat_bottom = (0,5),(10,11),(17.5,11),(20.5,9.5),(21.875,8.0),(31.0,8.0)


#                 1      2       3      4      5       6       7      8       9       10      11     12       13     14      15       16      17      18,     19      20      21
stations     = [18.0,  22.0,   26.0,  31.0,  36.0,   43.0,   48.0,  58.0,   68.0,   79.0,   84.00, 91.0,   106.0, 126.0,  146.00,  170.00, 196.0,  224.0,  246.68, 247.02, 248.33 ]
widths       = [ 6.66,  7.89,   8.84,  9.79, 10.54,  11.34,  11.8,  12.43,  12.75,  12.83,  12.77, 12.61,  11.91,  10.40,   8.62,    6.67,   5.0,    3.64,   2.75,   2.75 ,  2.75]
upper_top    = [20.08, 23.09,  25.52, 28.02, 30.10,  32.48,  33.86, 35.92,  37.09,  37.30,  36.97, 36.39,  35.45,  34.53,  33.84,   33.15,  32.55,  32.0,   None,    None,  31.47]
upper_bottom = [14.0,  14.65,  15.32, 16.16, 17.00,  18.16,  19.00, 20.65,  22.32,  24.16,  25.0,  24.66,  24.01,  23.28,  22.69,   22.20,  22.0,   22.0,   None,   22.0,   30.0]
belly_top    = [14.0,  12.57,  11.59, 10.68, 10.01,  9.35,   9.04,  8.75,   9.07,   10.32,  None,  12.38,  14.90,  17.31,  18.78,   19.70,  20,     20,     20.0,    None,  None]
belly_bottom = [ 4.07, 3.13,    2.53,  2.02,  1.70,  1.5,    1.5,   1.87,   2.87,    4.54,  None,   6.75,   9.61,  12.46,  13.93,   15.17,  16.18,  16.97,   None,   None,  None]
floor_level  = [14.0,  8.0,     5.5,   5.5,   5.5,  10.0,   10.0,   5.0,    5.0]    



def mirrorz(points):
    points2 = []
    for i in points:
        points2.append(i)
        points2.append((i[0],i[1],i[2]*-1.0))
    return points2
def parallel(a,b):
    points2 = []
    for i in range(max(len(a),len(b))):
        if i < len(a):
            points2.append(a[i])
        if i < len(b):
            points2.append(b[i])
    return points2

cockpit_floor = [(stations[0], 12,                2  ),                # 1    # floor
                 (stations[1],  8,                widths[1]-2),        # 2
                 (stations[2],  5.5,              widths[2]-2),        # 3
                 (stations[3],  5.5,              widths[3]-2),        # 4
                 (stations[4],  5.5,              widths[4]-2),        # 5
                 # ---
                 (stations[5], 11.0,              widths[5]-2),        # 6
                 (stations[6], 11.0,              widths[5]-2),        # 7
                 # ---
                 (stations[7],  5.0,              seat_half_width),    # 8
                 (66.0,         5.0,              seat_half_width),       
                 (stations[8],  6.0,              seat_half_width),    # 9
                 (72.0,         8.0,              seat_half_width),
                 (stations[9],  8.0,              seat_half_width),    # 10
                ]
cockpit_sides = [(stations[0],  upper_bottom[0],   4.75),              # 1    #cockpit sill
                 (stations[1],  upper_bottom[1],   widths[1]-1),       # 2   
                 (stations[2],  upper_bottom[2],   widths[2]-1),       # 3   
                 (stations[3],  upper_bottom[3],   widths[3]-1),       # 4   
                 (stations[4],  upper_bottom[4],   widths[4]-1),       # 5   
                 # ---
                 (stations[5],  upper_bottom[5],   widths[5]-1),       # 6   
                 (stations[6],  console_height,    widths[6]-1),       # 7   
                 # ---
                 (stations[7],  console_height-.5, seat_half_width),   # 8   
                 (66.0,         console_height-.5, seat_half_width),       
                 (stations[8],  console_height-.5, seat_half_width),   # 9   
                 (72.0,         console_height-.5, seat_half_width),
                 (stations[9],  console_height-.5, seat_half_width),   # 10   
                 # ---
                 (stations[7],  console_height,   seat_half_width+1),  # 8   
                 (66.0,         console_height, seat_half_width+1),       
                 (stations[8],  console_height,   seat_half_width+1),  # 9   
                 (72.0,         console_height, seat_half_width+1),
                 (stations[9], console_height,   seat_half_width+1),   # 10   
               ]  
cockpit_sides.append((stations[5],upper_bottom[5],widths[5]))
for i in range(6,6+5): # 12 + 17-23                                           # add cockpit sill
    cockpit_sides.append((stations[i],console_height,widths[i]))

# --------------------------------------------------------
# cockpit floor
# --------------------------------------------------------
floor = mirrorz(cockpit_floor)
floor_shapes = []
for i in range(0,len(floor)-2,2):
    floor_shapes.append((i,i+1,i+3,i+2))
perimeter,fold_lines = flat_box(floor, floor_shapes,[])
print(points_to_poly(perimeter))
#print(floor)
#print(floor_shapes)



# --------------------------------------------------------
# cockpit sides, front
# --------------------------------------------------------
sides = parallel(cockpit_floor,cockpit_sides)
sides_shapes = []
for i in range(0,7*2-2,2):
    sides_shapes.append((i,i+1,i+2))
    sides_shapes.append((i+2,i+1,i+3))
sides_shapes.append((13,11,29,30))
#print(sides)
#5/0
perimeter,fold_lines = flat_box(sides, sides_shapes,[])
print(points_to_poly(perimeter))
for line in fold_lines:
    print(build_dashed_line(*line))

# --------------------------------------------------------
# cockpit sides, middle
# --------------------------------------------------------
sides_shapes = [ (12,12+1,12+3),
                 (12,12+3,12+2),
                 (15,13,24),
                 (24,13, 30,31)
                 ]
perimeter,fold_lines = flat_box(sides, sides_shapes,[],50,0)
print(points_to_poly(perimeter))
for line in fold_lines:
    print(build_dashed_line(*line))

# --------------------------------------------------------
# cockpit sides, aft
# --------------------------------------------------------
sides_shapes = [ (18,16,14,15,23,22,20),
                 (23,15,24,28),
                 (28,24,31,32,33)
               ]
perimeter,fold_lines = flat_box(sides, sides_shapes,[],70,0)
print(points_to_poly(perimeter))
for line in fold_lines:
    print(build_dashed_line(*line))

# --------------------------------------------------------
# canopy bottom/front strip
canopy_frame = [(20.46,22.02,0),
                (stations[1],20.4,5.76),                     # station 2
                (stations[2],18.54, 8.38),                   # station 3
                (stations[3],17.52, 9.62),                   # station 4
                (stations[4],17.29, 10.42),                  # station 5
                (39.75,17.62,11.0),
                (stations[5],upper_bottom[5],widths[5]),     # station 6
                # panel
                (42.42,26.0,6.0),
                (42.66,24.14,7.875), 
                (42.87,22.49,7.875),
                (43.0,21.5,6.875),
                # station 5
                (stations[4],24.81,7.0),
                (stations[4],19.0,8.625),
                # station 4
                (stations[3],23.34,0),
                (stations[3],17.51,widths[4]-1)]

canopy_frame = mirrorz(canopy_frame) 
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter([i[0] for i in canopy_frame],
           [i[1] for i in canopy_frame],
           [i[2] for i in canopy_frame])
plt.show()

# --------------------------------------------------------








# 10x10x10 cube
a = [(0,0,0),  (10,0,0),  (10,10,0),  (0,10,0),
     (0,0,10), (10,0,10), (10,10,10), (0,10,10)]

b = [(0,1,2,3), # top
     (1,0,4,5),
     (2,1,5,6),
     (3,2,6,7),
     (0,3,7,4),
     (4,7,6,5)
     ]



# this is a test for showing the side view (projection) of the fuselage.  just to make sure it's working
#side_projection = [(stations[i],upper_top[i]) for i in range(len(stations)) if upper_top[i]] + [(stations[i],belly_bottom[i]) for i in reversed(range(len(stations))) if belly_bottom[i]]
#print(points_to_poly(side_projection))

# this is a test for the flat_box function
#perimeter,fold_lines = flat_box(a,b,[])
#print(points_to_poly(perimeter))
#for line in fold_lines:
#    print(build_dashed_line(*line))

# first the top of the consoles
#for i in range(console_start,console_end+1):
#    if widths[i]:
#        console.append((widths[i]-(seat_width/2),stations[i]-stations[console_start]))
#for i in range(len(console)-1):
#    print(points_to_poly(make_tab(console[i],console[i+1])))
#
#console = [(console_edge_radius,console[0][1])] + console + [(console_edge_radius,console[-1][1])]
#print(build_dashed_line(console[0],console[-1]))
#console = [(console[0][0]-console_edge_unrolled,console[0][1])] + console + [(console[-1][0]-console_edge_unrolled,console[-1][1])]
#print(build_dashed_line(console[0],console[-1]))
#
## console sides (your legs go between these)
#for i in reversed(seat_bottom):
#    console.append((console[0][0]+1.5-i[1],i[0]))
#print(points_to_poly(console))





# spine
spine  = [(widths[i],stations[i]) for i in range(10,len(widths)-3)] 
spine += [(i[0]*-1,i[1]) for i in reversed(spine)]

# outline
print(points_to_poly(spine,tx=-16,ty=-280))

# cutouts & tabs
for i in range((len(spine)//2)-1):
    cutout = [spine[i],spine[i+1],spine[(-1 * i) - 2],spine[(-1 * i) -1]]
    print(points_to_poly(round_corners(cutout, -4,7,-5), tx=-16,ty=-280))

    print(points_to_poly(make_tab(spine[i],spine[i+1]), tx=-16,ty=-280))
    print(points_to_poly(make_tab(spine[(-1*i)-2],spine[(-1*i)-1]), tx=-16,ty=-280))




# --------------------------------------------------------------------------------------------------------



fuselage = []
for i in range(len(stations)):

    vertical_center   = upper_bottom[i]
    horizontal_center = 0
    width             = widths[i]
    height            = upper_bottom[i] - upper_top[i] if upper_top[i] else None
    datum             = stations[i]
    amount            = 0.5
    upper = {'vertical_center': vertical_center, 
             'horizontal_center': horizontal_center, 
             'width': width, 
             'height': height, 
             'datum': datum, 
             'amount': 0.5}

    vertical_center   = belly_top[i]
    horizontal_center = 0
    width             = widths[i]
    height            = belly_bottom[i] - belly_top[i] if belly_bottom[i] else None
    datum             = stations[i]
    amount            = 0.5
    lower = {'vertical_center': vertical_center, 
             'horizontal_center': horizontal_center, 
             'width': width, 
             'height': height, 
             'datum': datum, 
             'amount': 0.5}

    fuselage.append({'upper': upper,
                     'lower': lower})

# fuselage top & bottom
lowers = ellipses([i['lower'] for i in fuselage if i['lower']['height']], flip=False)
uppers = ellipses([i['upper'] for i in fuselage if i['upper']['height']], 50, flip=True)
#for i in fuselage:
#    print (i['upper'])
#print (uppers)
#5/0 

# tail triangle
da = distance((stations[-4],upper_bottom[-4],widths[-4]),
              (stations[-2],upper_bottom[-2],widths[-2]))

db = distance((stations[-1],upper_bottom[-1],widths[-1]),
              (stations[-2],upper_bottom[-2],widths[-2]))
print(da)
print(db)

print(flat_triangle(uppers[-1][0][0],uppers[-1][1][-1],da,db,'right'))
print(flat_triangle(uppers[-1][0][-1],uppers[-1][1][0],da,db,'left'))


# connecting strips
for i in range(len(lowers)):
    a = lowers[i][0]
    b = lowers[i][1]
    print(a[0])
    print(b[-1])
    anglea = math.atan2(a[0][0]-b[-1][0], a[0][1]-b[-1][1])
    angleb = math.atan2(a[-1][0]-b[0][0], a[-1][1]-b[0][1])

    a2 = (b[-1][0]+(flange_width*.5)*math.sin(anglea),         b[-1][1]+(flange_width*.5)*math.cos(anglea))
    b2 = (b[0][0]+(flange_width*.5)*math.sin(angleb), b[0][1]+(flange_width*.5)*math.cos(angleb))
    connecting_strip(a, [],
                     flange_width, 5)
    

# make the fuselage flat sides.
fuselage_sides = []

ub2 = upper_bottom[:10] + upper_bottom[11:]
bt2 = belly_top[:10] + belly_top[11:]
st2 = stations[:10] + stations[11:]
wd2 = widths[:10] + widths[11:]

old_width = 0.0
for i in range(len(ub2)-1):
    points = ''
    width = distance((st2[i], wd2[i]), 
                     (st2[i+1], wd2[i+1]))
    a = (ub2[i],   old_width,   wd2[i])
    b = (bt2[i],   old_width,   wd2[i])
    c = (ub2[i+1], old_width+width, wd2[i+1])
    d = (bt2[i+1], old_width+width, wd2[i+1])


    # full projected sides
    if c[0] and d[0]:
        points = [a,b,
                  (d[0],b[1]+width),
                  (c[0],a[1]+width)]
        print(points_to_poly(points,tx=-66,ty=-230))



    if (not a[0]) or (not b[0]) or (not c[0]):
        continue
    # sides minus half connecting strip width
    points = [a, (b[0]-flange_width,b[1]),
              (d[0]-flange_width,b[1]+width),
              (c[0],a[1]+width)]
    print(points_to_poly(points,tx=-66,ty=-230))


    # connecting strip...
    if d[0] and c[0]:
        points = [(b[0]-flange_width*2,b[1]),
                  (b[0],b[1]),

                  (d[0],a[1]+width),
                  (d[0]-flange_width*2,a[1]+width)]
        print(points_to_poly(points,tx=-66,ty=-230))
    old_width += width





airfoil1 = load_airfoil('GA40-A620.dat')
airfoil2 = load_airfoil('GA40-A618.dat')
airfoil3 = load_airfoil('GA40-A616.dat')
airfoil4 = load_airfoil('NACA-0012.dat')

#airfoil2 = load_airfoil('GA40-A610.dat')

# the wing
percent_chord_spar  = 0.4
percent_chord_spar2 = 0.65
a620_spar_extents   = [-0.05539,0.14396]
a620_spar2_extents  = [-0.03769,0.10639]
a618_spar_extents   = [-0.04539,0.13011]
a618_spar2_extents  = [-0.03048,0.09918]
a616_spar_extents   = [-0.03539,0.12455]
a616_spar2_extents  = [-0.02328,0.09198]
root_chord          = 48
chord_a             = 382.5-338.8
chord_b             = 380.3-342.9
chord_c             = 376.65-349.9
chord_d             = 372.92-356.93
offset_a            = (root_chord*.4)-(chord_a*.4)
offset_b            = (chord_a*.4)-(chord_b*.4)
offset_c            = (chord_b*.4)-(chord_c*.4)
offset_d            = (chord_c*.4)-(chord_d*.4)



# wing
spanlines = [0.0,0.4,0.65]
wing_skin(airfoil1, root_chord, airfoil2, chord_a, 36, offset_a, tx=-140, ty=0, spanlines=spanlines)
wing_skin(airfoil2, chord_a, airfoil3,    chord_b, 52, offset_b, tx=-140, ty=-40, spanlines=spanlines)
wing_skin(airfoil3, chord_b, airfoil3,    chord_c, 90, offset_c, tx=-140, ty=-95, spanlines=spanlines)
wing_skin(airfoil3, chord_c, airfoil3,    chord_d, 90, offset_d, tx=-140, ty=-190, spanlines=spanlines)

#spars
wing_spar(root_chord,chord_a,36,a620_spar_extents,a618_spar_extents,tx=-180,ty=-250)
wing_spar(chord_a,chord_b,52,a618_spar_extents,a616_spar_extents,tx=-180,ty=-250+36)
wing_spar(chord_b,chord_c,90,a616_spar_extents,a616_spar_extents,tx=-180,ty=-250+36+52)
wing_spar(chord_c,chord_d,90,a616_spar_extents,a616_spar_extents,tx=-180,ty=-250+36+52+90)



#vtail_curve = wing_skin(airfoil4, 42.65, airfoil4, 17.625, 28, 18.5)[0][50:90]
vtail_base,vtail_top,vtail_skin = wing_skin(airfoil4, 42.65, airfoil4, 17.625, 28, 18.5, tx=180,ty=-200)
vstab_lower_curve  = vtail_base[47:90]
vstab_middle_curve = vtail_base[50:-50]
vstab_upper_curve  = vtail_top[50:-50]

# translate
def transform_tail(coords, transx, y):
    for i in range(len(coords)):
        coords[i] = (coords[i][0]+transx, y, coords[i][1])
    return coords

def flip_z(coords):
    return [(i[0],i[1],i[2]*-1.0) for i in reversed(coords)]

transform_tail(vstab_lower_curve, 217.5, 22)
transform_tail(vstab_middle_curve, 217.5, 22)
transform_tail(vstab_upper_curve, 217.5, -6)

vstab_lower_curve.insert(0,(241.24,22,2.06)) # aft top
#vstab_lower_curve.insert(0,(236.01,42,2.75)) # aft bottom


vstab_lower_curve.insert(0,(238.61,42,2.37))

vstab_middle_curve.insert(0,(241.24, 22,  2.06))
vstab_middle_curve.append(  (241.24, 22, -2.06))

vstab_upper_curve.insert(0,(244.93,-6,.91))
vstab_upper_curve.append(  (244.93,-6,-.91))

# lower vertical stabilizer
build_flat_fan((213,42,4.6),vstab_lower_curve, tx=160, ty=-20)
# upper vertical stabilizer
build_flat_shape(vstab_middle_curve,vstab_upper_curve,tx=140,ty=-40)




# rudder
# the single most complicated part of this whole thing.

rudder_lower_end = [(254.57,42,0)]
rudder_bottom_end = [(251.91,44,0)]

rudder_front_bottom = make_ellipse({'width':             2.163,
                                    'height':            2.163,
                                    'datum':             239.0,
                                    'horizontal_center': 0,
                                    'vertical_center':   44,
                                    'amount':            0.5},
                                    numsteps=20, mode=2, flip=2)
rudder_front_lower  = make_ellipse({'width':             2.251,
                                     'height':            2.251,
                                     'datum':             239.26,
                                     'horizontal_center': 0,
                                     'vertical_center':   42,
                                     'amount':            0.5},
                                     numsteps=20, mode=2, flip=2)
rudder_front_middle  = make_ellipse({'width':             2.012,
                                     'height':            2.012,
                                     'datum':             241.8,
                                     'horizontal_center': 0,
                                     'vertical_center':   22,
                                     'amount':            0.5},
                                     numsteps=20, mode=2, flip=2)
rudder_front_upper   = make_ellipse({'width':             .881,
                                     'height':            .881,
                                     'datum':             244.93,
                                     'horizontal_center': 0,
                                     'vertical_center':   -6,
                                     'amount':            0.5},
                                     numsteps=20, mode=2, flip=2)

rudder_middle_curve  = vtail_base[0:46]
rudder_upper_curve   = vtail_top[0:46]
transform_tail(rudder_middle_curve,217.5,22)
transform_tail(rudder_upper_curve,217.5,-6)

rudder_middle = rudder_middle_curve + rudder_front_middle + flip_z(rudder_middle_curve)
rudder_upper = rudder_upper_curve + rudder_front_upper + flip_z(rudder_upper_curve)

print(points_to_poly(rudder_middle,xindex=0,yindex=2,tx=-110,ty=-250))
print(points_to_poly(rudder_upper,xindex=0,yindex=2,tx=-110,ty=-240))

# rudder top
build_flat_shape(rudder_middle,rudder_upper,tx=130,ty=-170)

# rudder middle
a=build_flat_fan((239.26,42,2.28),rudder_lower_end+rudder_middle_curve+[(241.8,22,2.02)],tx=160,ty=-140)
b=build_flat_shape(rudder_front_lower, rudder_front_middle, start=a,tx=160,ty=-140)
c=build_flat_fan((239.26,42,2.28),rudder_lower_end+rudder_middle_curve+[(241.8,22,2.02)],start_pivot=b[1][-1],start_point=b[2][0],reverse=True,tx=160,ty=-140)

# rudder lower
build_flat_shape(rudder_lower_end+rudder_front_lower+rudder_lower_end,
                 rudder_bottom_end+rudder_front_bottom+rudder_bottom_end,hoffset=140,voffset=-80)

print(points_to_poly(rudder_lower_end+rudder_front_lower+rudder_lower_end,
                     xindex=0,yindex=2,tx=-110,ty=-230))
print(points_to_poly(rudder_bottom_end+rudder_front_bottom+rudder_bottom_end,
                     xindex=0,yindex=2,tx=-110,ty=-220))
# horizontal tail
a = 25*.3
b = 18*.3
wing_skin(airfoil4, 25, airfoil4, 18, 62, a-b,tx=180,ty=-100)





# make bulkheads
for i in range(len(fuselage)):
    tx = 110
    ty = -350+i*30
    station = fuselage[i]
    #points = ''
    points = [] 
    if station['upper']['height']:
        upper = make_ellipse(station['upper'], flip=True)
        upper = [(i[2],i[1]) for i in upper]
        points += upper
        connecting_strip(upper,[],flange_width, 4, tx=tx,ty=ty)
    else:
        if station['upper']['width'] and station['upper']['vertical_center']:
            points.append((station['upper']['width'],
                           station['upper']['vertical_center']))
            points.append((station['upper']['width']*-1.0,
                           station['upper']['vertical_center']))

    if station['lower']['height']:
        lower = make_ellipse(station['lower'])
        lower = [(i[2],i[1]) for i in lower]
        lower.reverse()
        points += lower
        connecting_strip(lower,[],flange_width, 4, tx=tx,ty=ty)

    if points:
        print(points_to_poly(points, tx=tx,ty=ty))

print('</svg>')    



