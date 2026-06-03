







# sheet metal constants 
flange_width          = .75
ellipse_steps         = 401


# fuselage bulkheads
#                  0       1       2      3      4       5       6     7      8      9     10     11      12     13      14      15      16      17     18,     19      20      21 
stations        = [18.0,  22.0,   26.0,  31.0,  36.0,   43.0,  48.0,  58.0,  68.0,  79.0,  84.00, 91.0,  106.0, 126.0,  146.00, 170.00, 196.0,  220.0, 246.38, 246.68, 247.02,  248.33 ]
widths          = [ 6.66,  7.89,   8.84,  9.79, 10.54,  11.34, 11.8,  12.43, 12.75, 12.83, 12.77, 12.61, 11.91,  10.40,   8.62,   6.67,   5.0,    3.8,   2.83,   2.83,   2.83 ,  2.575 ]
upper_top       = [20.08, 23.09,  25.52, 28.02, 30.10,  32.48, 33.86, 35.92, 37.09, 37.30, 36.97, 36.39, 35.45,  34.53,  33.84,  33.15,  32.55,  32.09,  None,  None,    None,  31.47  ]
upper_bottom    = [14.0,  14.65,  15.32, 16.16, 17.00,  18.16, 19.00, 20.65, 22.32, 24.16, 25.0,  24.66, 24.01,  23.28,  22.69,  22.20,  22.0,   22.0,   22.0,  22.0,   22.0,    30.0  ]
skin_split      = [None,  -1,     -1,    -1,    -1,     -1,    -1,    -1,    -1,    -1,    22.82, 21.0,  21.0,   21.0,   21.0,   21.0,   21.0,   21.0,   None,  None,   None,    None  ]
bulkhead_split  = [None,  -1,     -1,    -1,    -1,     -1,    -1,    -1,    -1,    -1,    20.0,  20.0,  20.0,   20.0,   20.0,   20.0,   20.0,   20.0,   20.0,  20.0,   20.0,    20.0  ]
belly_top       = [14.0,  12.57,  11.59, 10.68, 10.01,  9.35,  9.04,  8.75,  9.07,  10.32, None,  12.38, 14.90,  17.31,  18.78,  19.70,  20,     20,     20.0,  20.0,   20.0,    20.0  ]
belly_bottom    = [ 4.07, 3.13,    2.53,  2.02,  1.70,  1.5,   1.5,   1.87,  2.87,   4.54, None,   6.75,  9.61,  12.46,  13.93,  15.17,  16.18,  17.0,   18.24, None,   None,    None  ]
bulkhead_top    = [True,  False,   False, False, False, False, False, False, False, False, True,  True,  True,  True,    True,   True,   True,   True,    True, True,   True,    True  ]  
skin_thickness  = [  .02,  .02,     .02,   .02,   .02,   .02,   .02,   .02,   .02,    .02,   .02,   .02,   .02,    .02,    .02,    .02,    .02,    .02,    .02,   .02,    .02,     .02 ]
conn_thickness  = [  .02,  .02,     .02,   .02,   .02,   .02,   .02,   .02,   .02,    .02,   .02,   .02,   .02,    .02,    .02,    .02,    .02,    .02,    .02,   .02,    .02,     .02 ]
bulk_thickness  = [  .02,  .02,     .02,   .02,   .02,   .02,   .02,   .02,   .02,    .02,   .02,   .02,   .02,    .02,    .02,    .02,    .02,    .02,    .02,   .02,    .02,     .02 ]

top_notches     = [ [],              [0,2,2],         [],              [],              [],              
                    [],              [],              [],              [],              [], 
                    [0,2,3,3,3,3,2,2,2], [1,2,3,3,3,3,2,1], [1,2,3,3,3,3,2],   [1,3,3,3,3,2,1],   [1,3,3,3,2,2,1],
                    [1,3,3,3,2,1],     [1,3,3,2,1,1],     [1,3,2,2,1,1],     [],              [],
                    [], [] ]

bottom_notches  = [ [],                [1,3,2,2,2,1,1],         [1,1,2,3,3,3],       [1,1,1,2,3,2,2],   [1,1,1,2,2,3,3],
                   [1,1,1,2,2,3,3], [1,1,1,2,2,3,3],   [1,1,1,2,2,3,3], [1,1,1,2,2,3,3], [1,1,1,2,2,3,3],
                   [],                [1,1,1,2,3,3,3], [1,1,1,2,3,3],   [1,1,1,2,3,3],       [1,1,1,2,3],
                    [0,1,2,3],       [0,1,1,2],       [1,1,1,2],     [],                  [],
                    [], [] ]



# cockpit constants
seat_width            = 18
seat_half_width       = seat_width/2.0
console_height        = 14






# vstab/rudder y position (height):
rudder_y_upper     = 70
rudder_y_middle    = 42
rudder_y_lower     = 22
rudder_y_bottom    = 20
rudder_y_bottomest = 18.25

# points in the vstab...

# these used to be station[-5], but I moved that forward.
# TODO: make this another bulkhead instead?
vstab_front_bottom = [(stations[-5], upper_bottom[-5], widths[-5]),
                      (stations[-5], belly_top[-5],    widths[-5])]

vstab_middle_post_pos = (250.31, rudder_y_middle,  2.2)
vstab_middle_post_neg = (250.31, rudder_y_middle, -2.2)
vstab_lower_post_pos  = (stations[-2],upper_bottom[-2],widths[-2])
vstab_lower_post_neg  = (stations[-2],upper_bottom[-2],widths[-2]*-1)
vstab_bottom_post_pos = (stations[-3],belly_top[-3],widths[-3])
vstab_middle_end_pos  = (252.24, rudder_y_middle,  2.06)
vstab_middle_end_neg  = (252.24, rudder_y_middle, -2.06)

vstab_lower_end_pos   = (249.72, rudder_y_lower,   2.75)      
vstab_lower_end_neg   = (249.72, rudder_y_lower,  -2.75)     
vstab_bottom_end_pos  = (249.46, rudder_y_bottom,  2.75)    
vstab_bottom_end_neg  = (249.46, rudder_y_bottom, -2.75)    
vstab_lowest_end_pos  = (249.25, 18.41,            2.75)   
vstab_lowest_end_neg  = (249.25, 18.41,           -2.75)  

vstab_upper_end_pos   = (255.93,rudder_y_upper,.91)
vstab_upper_end_neg   = (255.93,rudder_y_upper,-.91)


cockpit_floor = [(stations[0],  12,                          3  ),                # 1    # floor
                 (stations[1],  8,                           widths[1]-2.25),     # 2
                 (stations[2],  6.0,                         widths[2]-2.25),     # 3
                 (stations[3],  6.0,                         widths[3]-2.25),     # 4
                 (stations[4],  6.0,                         widths[4]-2.25),     # 5
                 # ---
                 (stations[5],  11.0,                        seat_half_width),     # 6
                 (stations[6],  11.0,                        seat_half_width),     # 7
                 # ---
                 (stations[7],  5.0,                         seat_half_width),    # 8
                 (66.0,         5.0,                         seat_half_width),       
                 (stations[8],  6.0,                         seat_half_width),    # 9
                 (72.0,         8.0,                         seat_half_width),
                 (stations[9],  8.0,                         seat_half_width),    # 10
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
                 (stations[7],  console_height,    seat_half_width+1),  # 8   
                 (66.0,         console_height,    seat_half_width+1),       
                 (stations[8],  console_height,    seat_half_width+1),  # 9   
                 (72.0,         console_height,    seat_half_width+1),
                 (stations[9],  console_height,    seat_half_width+1),   # 10   
               ]  

cockpit_sides.append((stations[5],upper_bottom[5],widths[5]))

for i in range(6,6+5): # 12 + 17-23                                           # add cockpit sill
    cockpit_sides.append((stations[i], console_height, widths[i]))





# wing constants
# --------------------------------------------------------------------------------------------------------

wing_percent_chord_spar  = 0.37
wing_percent_chord_spar2 = 0.70
wing_percent_chord_trim  = 0.73
wing_percent_chord_flap  = 0.75


# TODO: calculate these from the line equation, instead of
#       copying them off of the plan...
wing_chords = [ 48,
           382.5-338.8,
           380.3-342.9,
           376.65-349.9,
           372.92-356.93]

wing_spans = [36,52,90,90]
wing_vloc = [0,-40,-95,-190]
wing_num_ribs = [4,4,7,6]

wing_spanlines = [[0.0,wing_percent_chord_spar,wing_percent_chord_spar2],[]]





# horizontal tail
# --------------------------------------------------------------------------------------------------------

tail_percent_leading_edge = 0.0
tail_percent_spar         = 0.6

htail_chords = [25,18]

tail_a = htail_chords[0]*tail_percent_spar
tail_b = htail_chords[1]*tail_percent_spar
tail_spanlines=[[0.0,tail_percent_spar],[]]
