import math

from flat_wrap import *

#                 1       2      3      4      5       6       7      8       9       10       11     12        13       14      15      16       17     18
stations     = [12.0,   17.0,  22.5,  28.0,  35.0,   43.0,   48.0,  58.0,   68.0,   79.0,    84.00,  91.0,   104.0,   126.0,  161.00,  213.0,   235.5, 237.27 ]
widths       = [ 6.03,  7.69,   8.93,  9.86, 10.75,  11.50,  11.86, 12.375, 12.67,  12.85,   12.85,  12.85,   12.56,   11.5,    8.69,    3.875,   2.0,   2.0  ]

upper_top    = [42.75, 39.375, None,  None,  None,   None,   None,  None,   None,   None,    27.00,  28.04,   29.31,   30.34,   30.91,  32.0,    None,  None  ]
upper_bottom = [48,    47.375, 46.69, 46.0,  45.125, 44.125, 43.5,  42.25,  41.0,   39.625,  39.0,   39.375,  40.375,  41.625,    42.0,   42.0,    None,  None  ]
                                                                                          
belly_top    = [48,    49.68,  51.12, 52.30, 53.48,  54.46,  54.88, 55.34,  55.03,  53.44,   None,   51.06,   48.52,   45.53,   44.0,   44.0,    None,  None  ]
belly_bottom = [57.75, 59.05,  60.06, 60.75, 61.29,  61.5,   61.5,  61.08,  60.33,  59.12,   None,   57.18,   54.97,   52.09,   49.59,  47.0,    None,  None  ]





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


# make the fuselage flat sides.
fuselage_sides = []

ub2 = upper_bottom[:10] + upper_bottom[11:]
bt2 = belly_top[:10] + belly_top[11:]
st2 = stations[:10] + stations[11:]
wd2 = widths[:10] + widths[11:]

for i in range(len(ub2)-1):
    points = ''
    a = (ub2[i],   st2[i],   wd2[i])
    b = (bt2[i],   st2[i],   wd2[i])
    c = (ub2[i+1], st2[i+1], wd2[i+1])
    d = (bt2[i+1], st2[i+1], wd2[i+1])
    width = distance((st2[i], wd2[i]), 
                     (st2[i+1], wd2[i+1]))

    #points += '{},{} \n'.format(a[0],a[1])
    #points += '{},{} \n'.format(b[0],b[1])
    #points += '{},{} \n'.format(d[0],b[1]-width)
    #points += '{},{} \n'.format(c[0],a[1]-width)
    points = [a,b,
              (d[0],b[1]-width),
              (c[0],a[1]-width)]
    print(points_to_poly(points))

# make bulkheads
for station in fuselage:
    points = ''
   
    if station['upper']['height']:
        upper = make_ellipse(station['upper'], flip=True)
        upper = [(i[0],i[1]) for i in upper]
        for j in upper:
            points += '{},{} \n'.format(j[0],j[1])
    else:
        points += '{},{} \n'.format(station['upper']['width'],
                                    station['upper']['vertical_center'])
        points += '{},{} \n'.format(station['upper']['width']*-1.0,
                                    station['upper']['vertical_center'])

    if station['lower']['height']:
        lower = make_ellipse(station['lower'])
        lower = [(i[0],i[1]) for i in lower]
        lower.reverse()
        for j in lower:
            points += '{},{} \n'.format(j[0],j[1])

    if points:
        print('<polygon stroke-width="0.1" fill="none" stroke="black" points="{}" />'.format(points))

#ellipses(upper_fuselage)
ellipses([i['lower'] for i in fuselage if i['lower']['height']])
ellipses([i['upper'] for i in fuselage if i['upper']['height']])

airfoil1 = load_airfoil('GA40-A620.dat')
airfoil2 = load_airfoil('GA40-A618.dat')
airfoil3 = load_airfoil('GA40-A616.dat')
airfoil4 = load_airfoil('NACA-0012.dat')

a = 25*.3
b = 18*.3
htail    = wing_skin(airfoil4, 25, airfoil4, 18, 62, a-b)
#airfoil2 = load_airfoil('GA40-A610.dat')

# the wing
root_chord = 48
chord_a    = 382.5-338.8
chord_b    = 380.3-342.9
chord_c    = 376.65-349.9
chord_d    = 372.92-356.93
offset_a   = (root_chord*.4)-(chord_a*.4)
offset_b   = (root_chord*.4)-(chord_b*.4)
offset_c   = (root_chord*.4)-(chord_c*.4)
offset_d   = (root_chord*.4)-(chord_d*.4)

wing_skin(airfoil1, root_chord, airfoil2, chord_a, 36,offset_a)
wing_skin(airfoil2, chord_a, airfoil3, chord_b, 52,offset_a)
wing_skin(airfoil3, chord_b, airfoil3, chord_c, 90,offset_a)
wing_skin(airfoil3, chord_c, airfoil3, chord_d, 90,offset_a)

wing_rib(airfoil4, 3600)

print('</svg>')    



