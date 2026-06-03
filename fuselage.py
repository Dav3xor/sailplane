import math
import constants

from flat_wrap import * # general dimensions:
from rivets import *
import numpy as np
import matplotlib.pyplot as plt


# things TODO:
# * ailerons, flaps...
# * update wing panels
# cockpit panel & shroud
# * ribs
# bulkheads
# spar shear/moment calculations
# surface area
# weights, balance, etc
# rivet holes



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

class Stations:
    def __getitem__(self,key):
        return self.get_thing(key)
    def __contains__(self,key):
        if key in self.stations:
            return self.get_thing(key)
        elif key in self.i_to_s:
            return self.get_thing(key)
        else:
            return None
    def get_thing(self, station):
        if type(station) == float:
            return self.stations[station]
        else:
            return self.stations[self.i_to_s[station]]
    
    def __init__(self):
        self.stations = {}
        self.i_to_s   = {}

    def get_bulkheads(self):
        return [key for key in self.stations if 'bulkhead_number' in self.stations[key]]

    def get_upper_ellipse(self,station):
        bulkhead          = self.get_thing(station)
        vertical_center   = bulkhead['upper_bottom']
        horizontal_center = 0
        width             = bulkhead['width']
        height            = bulkhead['upper_bottom'] - bulkhead['upper_top'] if bulkhead['upper_top'] else None
        datum             = bulkhead['station']
        amount            = 0.5
        skin_split        = bulkhead['skin_split']
        return {'vertical_center': vertical_center, 
                'horizontal_center': horizontal_center, 
                'width': width, 
                'height': height, 
                'datum': datum, 
                'skin_split': skin_split,
                'amount': 0.5}

    def get_lower_ellipse(self,station): 
        bulkhead          = self.get_thing(station)
        vertical_center   = bulkhead['belly_top']
        horizontal_center = 0
        width             = bulkhead['width']
        height            = bulkhead['belly_bottom'] - bulkhead['belly_top'] if bulkhead['belly_bottom'] else None
        datum             = bulkhead['station']
        amount            = 0.5
        skin_split        = bulkhead['skin_split']
        return {'vertical_center': vertical_center, 
                'horizontal_center': horizontal_center, 
                'width': width, 
                'height': height, 
                'datum': datum, 
                'skin_split': skin_split,
                'amount': 0.5}

    def add(self, station_loc, **kwargs):
        if 'bulkhead_number' in kwargs:
            bulkhead_number = kwargs['bulkhead_number']
            if bulkhead_number not in self.i_to_s:
                self.i_to_s[bulkhead_number]=station_loc
            else:
                if station_loc != self.i_to_s[bulkhead_number]:
                    print('WARNING: station numbers differ.')
                    print(f'WARNING: station_number = {station_number}, {station_loc} != {self.i_to_s[station_number]}')
                    5/0
        if station_loc not in self.stations:
            self.stations[station_loc] = {}
        self.stations[station_loc].update(kwargs)

                    


# --------------------------------------------------------
# build stations
# --------------------------------------------------------

s = Stations()

# bulkheads
for i in range(len(constants.stations)):
    station = constants.stations[i]
    data = {'bulkhead_number':i}
    data['station']      = constants.stations[i]
    data['width']        = constants.widths[i]
    data['upper_top']    = constants.upper_top[i]

    if constants.bulkhead_split[i] == -1:
        data['bulkhead_split']  = constants.upper_bottom[i]
    else:
        data['bulkhead_split']  = constants.bulkhead_split[i]
    
    if constants.skin_split[i] == -1:
        data['skin_split']  = constants.upper_bottom[i]
    else:
        data['skin_split']  = constants.skin_split[i]

    data['upper_bottom']   = constants.upper_bottom[i]
    data['belly_top']      = constants.belly_top[i]
    data['belly_bottom']   = constants.belly_bottom[i]
    data['bulkhead_top']   = constants.bulkhead_top[i]
    data['top_notches']    = constants.top_notches[i]
    data['bottom_notches'] = constants.bottom_notches[i]

    s.add(station,**data)

for station in constants.cockpit_floor:
    s.add(station[0], floor=station[1:])





# cockpit (in)sides
# these extra points cut the middle out of the lower bulkheads in the cockpit area
for i in range(1,7):
    bulkhead = s[i]
    s.add(constants.cockpit_sides[i][0], sides = [(bulkhead['width'],               bulkhead['bulkhead_split']-constants.flange_width),
                                                  (bulkhead['width']-constants.flange_width,           bulkhead['bulkhead_split']-constants.flange_width),
                                                  (constants.cockpit_floor[i][2],   constants.cockpit_floor[i][1])])
for i in range(7,12):
    if constants.cockpit_sides[i][0] in s and 'width' in s[constants.cockpit_sides[i][0]]:
        bulkhead = s[constants.cockpit_sides[i][0]]

        s.add(constants.cockpit_sides[i][0], sides = [(bulkhead['width'],               constants.cockpit_sides[i+5][1]),
                                                      (constants.cockpit_sides[i+5][2],           constants.cockpit_sides[i+5][1]),
                                                      (constants.cockpit_sides[i][2],             constants.cockpit_sides[i][1]),
                                                      (constants.cockpit_floor[i][2],   constants.cockpit_floor[i][1])])


# --------------------------------------------------------
# cockpit floor
# --------------------------------------------------------
floor = mirrorz(constants.cockpit_floor)
floor_shapes = []
for i in range(0,len(floor)-2,2):
    floor_shapes.append((i,i+1,i+3,i+2))
perimeter,fold_lines = flat_box(floor, floor_shapes,[])
print(perimeter)



# --------------------------------------------------------
# cockpit sides, front
# --------------------------------------------------------
sides = parallel(constants.cockpit_floor,constants.cockpit_sides)
sides_shapes = []
for i in range(0,7*2-2,2):
    sides_shapes.append((i,i+1,i+2))
    sides_shapes.append((i+2,i+1,i+3))
sides_shapes.append((13,11,29,30))

perimeter,fold_lines = flat_box(sides, sides_shapes,[])
print(perimeter)
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
print(perimeter)
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
print(perimeter)
for line in fold_lines:
    print(build_dashed_line(*line))

# --------------------------------------------------------
# canopy bottom/front strip
canopy_frame = [(20.46,22.02,0),
                (constants.stations[1], 20.4,                      5.76),                # station 2
                (constants.stations[2], 18.54,                     8.38),                # station 3
                (constants.stations[3], 17.52,                     9.62),                # station 4
                (constants.stations[4], 17.29,                     10.42),               # station 5
                (39.75,                 17.62,                     11.0),
                (constants.stations[5], constants.upper_bottom[5], constants.widths[5]), # station 6
                # panel
                (42.42,                 26.0,                      6.0),
                (42.66,                 24.14,                     7.875), 
                (42.87,                 22.49,                     7.875),
                (43.0,                  21.5,                      6.875),
                # station 5
                (constants.stations[4], 24.81,                     7.0),
                (constants.stations[4], 19.0,                      8.625),
                # station 4
                (constants.stations[3], 23.34,                     0),
                (constants.stations[3], 17.51,                     constants.widths[4]-1)
               ]

canopy_frame = mirrorz(canopy_frame) 
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter([i[0] for i in canopy_frame],
           [i[1] for i in canopy_frame],
           [i[2] for i in canopy_frame])
#plt.show()

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
#print(side_projection)

# this is a test for the flat_box function
#perimeter,fold_lines = flat_box(a,b,[])
#print(perimeter)
#for line in fold_lines:
#    print(build_dashed_line(*line))



# --------------------------------------------------------------------------------------------------------
# spine
spine  = Polygon([(constants.widths[i],constants.stations[i]) for i in range(10,len(constants.widths)-3)] )
spine += [(i[0]*-1,i[1]) for i in reversed(spine)]

# outline
print(spine.translate(-16,-280))

# cutouts & tabs
for i in range((len(spine)//2)-1):
    cutout = [spine[i],spine[i+1],spine[(-1 * i) - 2],spine[(-1 * i) -1]]
    print(round_corners(cutout, -4,7,-5))

    print(make_tab(spine[i],spine[i+1]))
    print(make_tab(spine[(-1*i)-2],spine[(-1*i)-1]))




# --------------------------------------------------------------------------------------------------------
# fuselage skin


# fuselage top & bottom (skins only)

lowers = [s.get_lower_ellipse(i) for i in s.get_bulkheads()]
uppers = [s.get_upper_ellipse(i) for i in s.get_bulkheads()]
lowers = flattened_ellipses([i for i in lowers if i['height']],     flip=False)
uppers = flattened_ellipses([i for i in uppers if i['height']], 50, flip=True)

# this is a series of points defining where the skin splits at the last section of the tail
tail_split_pos  = translate_point(constants.vstab_lower_end_pos, (constants.vstab_lower_end_pos[0]-constants.vstab_bottom_end_pos[0])/-2.0, -1, 0)
tail_split_neg  = translate_point(constants.vstab_lower_end_neg, (constants.vstab_lower_end_neg[0]-constants.vstab_bottom_end_neg[0])/-2.0, -1, 0)

#tail bottom triangle
a = (constants.stations[-5],       constants.belly_bottom[-5],   0)
b = (constants.stations[-4],       constants.belly_bottom[-4],   constants.widths[-4])
c = (constants.stations[-4],       constants.belly_bottom[-4],   constants.widths[-4]*-1)
d = (constants.stations[-3],       constants.belly_top[-3],      constants.widths[-3])
e = (constants.stations[-3],       constants.belly_top[-3],      constants.widths[-3]*-1)
f = (constants.stations[-5],       constants.belly_top[-5],      constants.widths[-5])
g = (constants.stations[-5],       constants.belly_top[-5],      constants.widths[-5]*-1)

h = (constants.stations[-5],       constants.upper_bottom[-5]-1, constants.widths[-5])
i = (constants.stations[-5],       constants.upper_bottom[-5]-1, constants.widths[-5]*-1)

j = (split(constants.stations[-2], constants.stations[-3]),      constants.upper_bottom[-2]-1, constants.widths[-2])
k = (split(constants.stations[-2], constants.stations[-3]),      constants.upper_bottom[-2]-1, constants.widths[-2]*-1)




# --------------------------------------------------------------------------------------------------------
# tail top triangle
da = distance((constants.stations[-5],  constants.upper_bottom[-5],  constants.widths[-5]),
              (constants.stations[-2],  constants.upper_bottom[-2],  constants.widths[-2]))

db = distance((constants.stations[-1],  constants.upper_bottom[-1],  constants.widths[-1]),
              (constants.stations[-2],  constants.upper_bottom[-2],  constants.widths[-2]))

#print(da)
#print(db)

tri_a = flat_triangle(uppers[-1][0][0],   uppers[-1][1][-1], da, db, 'right')
tri_b = flat_triangle(uppers[-1][0][-1],  uppers[-1][1][0],  da, db, 'left')

l = [(constants.stations[-5],  constants.upper_bottom[-5],     constants.widths[-5]),
     (constants.stations[-5],  constants.upper_bottom[-5]-1,   constants.widths[-5])]

m = [(constants.stations[-2],  constants.upper_bottom[-2],     constants.widths[-2]),    
     j]

positive_vertical_side     = build_flat_shape(m, l, start=(tri_a[0],tri_a[2]))

l = [(constants.stations[-5],  constants.upper_bottom[-5],   constants.widths[-5]*-1),
     (constants.stations[-5],  constants.upper_bottom[-5]-1, constants.widths[-5]*-1)]

m = [(constants.stations[-2],  constants.upper_bottom[-2],   constants.widths[-2]*-1),
     k]

negative_vertical_side     = build_flat_shape(l, m, start=(tri_b[2],tri_b[0]))

print(tri_a)
print(tri_b)
print(positive_vertical_side[1]+positive_vertical_side[2])
print(negative_vertical_side[1]+negative_vertical_side[2])


# --------------------------------------------------------------------------------------------------------
# tail bottom
tail_ellipse          = make_ellipse(s.get_lower_ellipse(220.0),
                                     numsteps=99)
tail_ellipse_positive = tail_ellipse[:50]
tail_ellipse_negative = tail_ellipse[49:]


positive_side   = build_flat_fan(b,tail_ellipse_positive,
                                 tx=10,ty=-265,color='red')

bottom_triangle = flat_triangle(positive_side[-2],positive_side[-1],
                                distance(a,c),distance(b,c),
                                side='right')

negative_side   = build_flat_fan(c,tail_ellipse_negative,
                                 start_pivot=bottom_triangle[-1],
                                 start_point=bottom_triangle[0],
                                 color='green')

# this is the little chunk at the verticle part of the tail  that overlaps the front of the rudder
positive_vertical_triangle = flat_triangle(positive_side[0], positive_side[-1],
                                           distance(f, d), distance(b,d))

negative_vertical_triangle = flat_triangle(negative_side[-2],negative_side[-1],
                                           distance(g,e),distance(c,e),
                                           side='right')
                                        
positive_vertical_side     = build_flat_shape((f,h), (d,j), 
                                              start = (positive_vertical_triangle[2],
                                                       positive_vertical_triangle[0]))
negative_vertical_side     = build_flat_shape((e,k), (g,i), 
                                              start = (negative_vertical_triangle[0],
                                                       negative_vertical_triangle[2]) )

top                        = [j, tail_split_pos]
bottom                     = [b,constants.vstab_lowest_end_pos]
positive_vertical_end      = build_flat_shape(top, bottom,
                                              start = (positive_vertical_triangle[1],
                                                       positive_vertical_side[2][0] ))

top                        = [c,constants.vstab_lowest_end_neg]
bottom                     = [k, tail_split_neg]
negative_vertical_end      = build_flat_shape(top, bottom,
                                              start = (negative_vertical_side[1][1],
                                                       negative_vertical_triangle[1]) )

print(positive_vertical_triangle)
print(bottom_triangle)
print(negative_vertical_triangle)
print(positive_vertical_side[1]+positive_vertical_side[2])
print(negative_vertical_side[1]+negative_vertical_side[2])
print(positive_vertical_end[1]+positive_vertical_end[2])
print(negative_vertical_end[1]+negative_vertical_end[2])







# fuselage skin connecting strips
# --------------------------------------------------------------------------------------------------------
for i in range(len(lowers)):
    a = lowers[i][0]
    b = lowers[i][1]
    connecting_strip(a, [],
                     constants.flange_width, 5, flat_ends=lowers[i][2])
    
for i in range(len(uppers)):
    a = uppers[i][0]
    b = uppers[i][1]
    connecting_strip(a, [],
                     constants.flange_width, 5, flat_ends=uppers[i][2])

# make the fuselage vertical/flat sides.
# --------------------------------------------------------------------------------------------------------
fuselage_sides = []

ub2 = constants.upper_bottom[:10] + constants.upper_bottom[11:]
bt2 = constants.belly_top[:10] + constants.belly_top[11:]
st2 = constants.stations[:10] + constants.stations[11:]
wd2 = constants.widths[:10] + constants.widths[11:]

old_width = 0.0

side_points = []
side_faces = []

j=0
for i in range(len(ub2)):
    if ub2[i]==None or bt2[i]==None:
        continue
    side_points.append((st2[i],ub2[i],wd2[i]))
    side_points.append((st2[i],bt2[i],wd2[i]))
    side_faces.append((j*2,j*2+1,j*2+3,j*2+2))
    j+=1
print(side_points)
print(side_faces)
side_faces = side_faces[2:-4]
perimeter,fold_lines = flat_box(side_points, side_faces,[])
print(perimeter)



# wings
# --------------------------------------------------------------------------------------------------------
airfoils = [load_airfoil('GA37-618.dat'),
            load_airfoil('GA37-617.dat'),
            load_airfoil('GA37-616.dat'),
            load_airfoil('GA37-615.dat'),
            load_airfoil('GA37-614.dat')]

tail_airfoil = load_airfoil('NACA-0012.dat')

    

spar1_extents = []
spar2_extents = []
for airfoil in airfoils:
    spar1_extents.append(insert_airfoil_point(airfoil, constants.wing_percent_chord_spar)[0]) #find_airfoil_extents(airfoil1, percent_chord_spar)
    spar2_extents.append(insert_airfoil_point(airfoil, constants.wing_percent_chord_spar2)[0])







# first, the flaps...
flap_shapes = []
for i in range(len(airfoils)):
    flap_root_top, flap_root_bottom   = trim_airfoil_end(airfoils[i], constants.wing_percent_chord_flap)
    radius = (flap_root_top[-1][1] - flap_root_bottom[0][1])/2
    
    flap_root_front = [[i[0],i[-1]] for i in make_ellipse({'width':             radius,
                                                     'height':            radius,
                                                     'datum':             flap_root_top[-1][0],
                                                     'horizontal_center': flap_root_top[-1][1]-radius,
                                                     'vertical_center':   0,
                                                     'amount':            0.5},
                                                     numsteps=20, mode=2, flip=2)][1:-1]

    flap_shapes.append(flap_root_top+flap_root_front+flap_root_bottom)

for i in range(len(airfoils)-1):

    wing_skin([ trim_airfoil(airfoils[i], constants.wing_percent_chord_trim), flap_shapes[i] ], 
              constants.wing_chords[i], 
              [ trim_airfoil(airfoils[i+1], constants.wing_percent_chord_trim), flap_shapes[i+1] ], 
              constants.wing_chords[i+1], 
              constants.wing_spans[i], 
              (constants.wing_chords[i]*constants.wing_percent_chord_spar)-(constants.wing_chords[i+1]*constants.wing_percent_chord_spar), 
              num_ribs      = constants.wing_num_ribs[i], 
              tx            = -140, 
              ty            = constants.wing_vloc[i],    
              spanlines     = constants.wing_spanlines)


#front spars
for i in range(len(constants.wing_chords)-1):
    wing_spar(constants.wing_chords[i], 
              constants.wing_chords[i+1], 
              constants.wing_spans[i], 
              spar1_extents[i], 
              spar1_extents[i+1], 
              tx   = -180, 
              ty   = -250+sum(constants.wing_spans[:i]))

    wing_spar(constants.wing_chords[i], 
              constants.wing_chords[i+1], 
              constants.wing_spans[i], 
              spar2_extents[i], 
              spar2_extents[i+1], 
              tx   = -210, 
              ty   = -250+sum(constants.wing_spans[:i]))





# horizontal tail
# --------------------------------------------------------------------------------------------------------

tail_nose_extents   = insert_airfoil_point(tail_airfoil, constants.tail_percent_leading_edge)[0]
tail_spar_extents  = insert_airfoil_point(tail_airfoil, constants.tail_percent_spar)[0]


ele_root_top, ele_root_bottom   = trim_airfoil_end(tail_airfoil, constants.tail_percent_spar+.05)
radius = (ele_root_top[-1][1] - ele_root_bottom[0][1])/2

ele_root_front = [[i[0],i[-1]] for i in make_ellipse({'width':             radius,
                                                      'height':            radius,
                                                      'datum':             ele_root_top[-1][0],
                                                      'horizontal_center': ele_root_top[-1][1]-radius,
                                                      'vertical_center':   0,
                                                      'amount':            0.5},
                                                      numsteps=20, mode=2, flip=2)][1:-1]
ele_shape = ele_root_top+ele_root_front+ele_root_bottom

wing_skin([trim_airfoil(tail_airfoil,constants.tail_percent_spar+.05),ele_shape], constants.htail_chords[0], 
          [trim_airfoil(tail_airfoil,constants.tail_percent_spar+.05),ele_shape], constants.htail_chords[1], 
          62, constants.tail_a-constants.tail_b,tx=220,ty=-100,spanlines=constants.tail_spanlines)

wing_spar(25,18,62,tail_spar_extents,tail_spar_extents,tx=220,ty=-100)




# vertical stabilizer
# --------------------------------------------------------------------------------------------------------


# the upper half of the vertical stabilizer
# --------------------------------------------------------------------------------------------------------
vtail_base,vtail_top,vtail_skin = wing_skin([tail_airfoil], 42.65, [tail_airfoil], 17.625, 28, 18.5, tx=180,ty=-200)

vstab_middle_curve = vtail_base[50:-50]
vstab_upper_curve  = vtail_top[50:-50]

# translate
def transform_tail(coords, transx, y):
    for i in range(len(coords)):
        coords[i] = (coords[i][0]+transx, y, coords[i][1])
    return coords

def flip_z(coords):
    return [(i[0],i[1],i[2]*-1.0) for i in reversed(coords)]

transform_tail(vstab_middle_curve, 228.5, constants.rudder_y_middle)
transform_tail(vstab_upper_curve, 228.5, constants.rudder_y_upper)



vstab_middle_curve.insert(0,constants.vstab_middle_end_pos)
vstab_middle_curve.append(  constants.vstab_middle_end_neg)

vstab_upper_curve.insert(0,constants.vstab_upper_end_pos)
vstab_upper_curve.append(  constants.vstab_upper_end_neg)

# upper vertical stabilizer
hoff,a,b = build_flat_shape(vstab_middle_curve,
                            vstab_upper_curve,
                            tx=140,ty=-40)
print(a+b)

# lower vertical stabilizer (2, one per side...  just making the positive one)
# -------------------------------------------------------------------------------------------------------
vstab_lower_curve      = vtail_base[49:90]
transform_tail(vstab_lower_curve, 228.5, constants.rudder_y_middle)
vstab_lower_curve.insert(3, constants.vstab_middle_post_pos)
vstab_lower_curve.insert(0, constants.vstab_middle_end_pos)
vstab_lower_curve.insert(0, constants.vstab_lower_end_pos)
vstab_lower_curve.insert(0, constants.vstab_bottom_end_pos)
vstab_lower_curve.insert(0, constants.vstab_bottom_post_pos)
vstab_lower_curve.insert(0, constants.vstab_front_bottom[1])
vstab_lower_curve.reverse()

panel = build_flat_fan(constants.vstab_front_bottom[0],
                       vstab_lower_curve, 
                       tx=160, ty=-20)


# rudder
# the single most complicated part of this whole thing.
# --------------------------------------------------------------------------------------------------------


rudder_bottom_end = Polygon([(262.91, constants.rudder_y_bottom, 0)])
rudder_lower_end  = Polygon([(265.57, constants.rudder_y_lower,  0)])

rudder_front_bottom = make_ellipse({'width':              2.251,
                                    'height':             2.251,
                                    'datum':              250.0,
                                    'horizontal_center':  0,
                                    'vertical_center':    constants.rudder_y_bottom,
                                    'amount':             0.5},
                                   numsteps=20, mode=2,  flip=2)
rudder_front_lower  = make_ellipse({'width':              2.251,
                                     'height':            2.251,
                                     'datum':             250.26,
                                     'horizontal_center': 0,
                                     'vertical_center':   constants.rudder_y_lower,
                                     'amount':            0.5},
                                    numsteps=20, mode=2, flip=2)
rudder_front_middle  = make_ellipse({'width':             2.012,
                                     'height':            2.012,
                                     'datum':             252.8,
                                     'horizontal_center': 0,
                                     'vertical_center':   constants.rudder_y_middle,
                                     'amount':            0.5},
                                    numsteps=20, mode=2, flip=2)
rudder_front_upper   = make_ellipse({'width':             .881,
                                     'height':            .881,
                                     'datum':             255.93,
                                     'horizontal_center': 0,
                                     'vertical_center':   constants.rudder_y_upper,
                                     'amount':            0.5},
                                    numsteps=20, mode=2, flip=2)

# rudder post
post_points = [(constants.stations[-4],constants.rudder_y_bottomest,   constants.widths[-4]),
               (constants.stations[-4],constants.rudder_y_bottomest,   constants.widths[-4]*-1),
               (constants.stations[-3],constants.rudder_y_bottom,      constants.widths[-3]),
               (constants.stations[-3],constants.rudder_y_bottom,      constants.widths[-3]*-1),
               (constants.stations[-2],constants.rudder_y_lower,       constants.widths[-2]),
               (constants.stations[-2],constants.rudder_y_lower,       constants.widths[-2]*-1),
               (250.32, constants.rudder_y_middle,  2.2),
               (250.32, constants.rudder_y_middle, -2.2),
               (254.95, constants.rudder_y_upper,    .95),
               (254.95, constants.rudder_y_upper,   -.95)]

post_polys = [(0,1,3,2),
              (2,3,5,4),
              (4,5,7,6),
              (6,7,9,8)]

perimeter,fold_lines = flat_box(post_points, post_polys,[])
print(perimeter)


rudder_middle_curve  = Polygon(vtail_base[0:46])
rudder_upper_curve   = Polygon(vtail_top[0:46])

transform_tail(rudder_middle_curve,  228.5, constants.rudder_y_middle)
transform_tail(rudder_upper_curve,   228.5, constants.rudder_y_upper)

rudder_middle = rudder_middle_curve + rudder_front_middle + flip_z(rudder_middle_curve)
rudder_upper  = rudder_upper_curve + rudder_front_upper + flip_z(rudder_upper_curve)

# rudder top
hoff,a,b = build_flat_shape(rudder_middle,rudder_upper,tx=130,ty=-170)
print(a+b)

# rudder middle
a = build_flat_fan((250.26,constants.rudder_y_lower,2.28),
                   rudder_lower_end + rudder_middle_curve + [(252.8, constants.rudder_y_middle, 2.02)],
                   tx=160, ty=-140)

b = build_flat_shape(rudder_front_lower, rudder_front_middle, start=a)

print(b[1]+b[2])

c=build_flat_fan((250.26, constants.rudder_y_lower, 2.28),
                 rudder_lower_end + rudder_middle_curve + [(252.8,constants.rudder_y_middle,2.02)],
                 start_pivot = b[1][-1],
                 start_point = b[2][0],
                 reverse = True)

# rudder lower
hoff,a,b = build_flat_shape(rudder_lower_end+rudder_front_lower+rudder_lower_end,
                            rudder_bottom_end+rudder_front_bottom+rudder_bottom_end,
                            hoffset=140,voffset=-80)
print(a+b)

print(rudder_middle.reduce2d(0,2).translate(-110,-250))
print(rudder_upper.reduce2d(0,2).translate(-110,-240))


# these are the ribs for the rudder lower/bottom
print((rudder_lower_end+rudder_front_lower+rudder_lower_end).reduce2d(0,2).translate(-110,-230))
print((rudder_bottom_end+rudder_front_bottom+rudder_bottom_end).reduce2d(0,2).translate(-110,-220))



# fuselage bulkheads
# --------------------------------------------------------------------------------------------------------
for i in range(len(s.get_bulkheads())):
    bulkhead = s[i]
    tx = 110
    ty = -350+i*30
    points = Polygon()
  
    uppers = s.get_upper_ellipse(i)
    if uppers['height']:
        upper = make_ellipse(uppers, flip=True, numsteps=constants.ellipse_steps)
        upper = [(j[2],j[1]) for j in upper]
        points += upper
        if bulkhead['bulkhead_split']:
            points.append((uppers['width']*-1.0,
                          bulkhead['bulkhead_split']))
            points.insert(0,(uppers['width'],
                          bulkhead['bulkhead_split']))
            make_notched_bulkhead(points, bulkhead['bulkhead_split'], bulkhead['top_notches'],tx,ty, side='top')

            a = uppers['width']*1.05
            b = a*-.55
            c = b-.5


            print(points.translate(tx,ty).color('green'))
            print(round_corners(points, b,a,c))
    else:
        if uppers['width'] and uppers['vertical_center']:
            points.append((uppers['width'],
                           uppers['vertical_center']))
            points.insert(0,(uppers['width']*-1.0,
                           uppers['vertical_center']))

    lowers = s.get_lower_ellipse(i)
    if lowers['height']:
        lower = make_ellipse(lowers,numsteps=constants.ellipse_steps)
        lower = Polygon([(j[2],j[1]) for j in lower])
        if bulkhead['bulkhead_split']:
            points = lower 
            if 'floor' in bulkhead:
                for p in bulkhead['sides']:
                    #points.append((p[0]*-1.0, p[1]))
                    points.append((p[0]*-1.0, p[1]))

                for p in reversed(bulkhead['sides']):
                    #points.append(p)
                    points.append((p[0], p[1]))
            else:
                points.append((uppers['width']*-1.0,
                              bulkhead['bulkhead_split']))
                points.insert(0,(uppers['width'],
                              bulkhead['bulkhead_split']))
                
                # center cutout
                a = lowers['height']*1.2
                b = a*-.55
                c = b-2.2
                print(round_corners(points, b,a,c).translate(tx,ty))

            make_notched_bulkhead(points, bulkhead['bulkhead_split'], bulkhead['bottom_notches'],tx,ty)
            print(points.translate(tx,ty))
        

    if not bulkhead['bulkhead_split'] and points: 
        lower.reverse()
        print(type(points))
        points += lower
        print(points.translate(tx,ty))

print('</svg>')    



