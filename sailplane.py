# airfoils to try:  NACA 633-618
#                   NACA 652-415
#                   SM701
#                   UAG 88-143/20
#                   Selig S8052


from statistics import mean
from svgpathtools import parse_path

pi             = 3.14159
tau            = 2*pi



Empty_Weight   = 180.0              # kilograms
Pilot_Weight   = 120.0              # kilograms 
Payload_Weight = 5.0                # kilograms 

TOW            =  Empty_Weight + Pilot_Weight + Payload_Weight

# fuselage
Fuselage_Width = 25.0  #inches
Fuselage_Frontal_Area = ( (6 * Fuselage_Width) + 
                          (pi * (Fuselage_Width/2.0) * 13)/2.0 + 
                          (pi * (Fuselage_Width/2.0) * 16) ) / 1550.0 # square meters
Fuselage_Drag_Coefficient = 0.045 # (Wild Ass Guess from Stelio Frati's book

# wings
Wingspan       =  15.0
Root_Chord     =  1.2192
Mid_Chord_1    =  1.04
Mid_Chord_2    =  0.800
Tip_Chord      =  0.381
Inner_Panel_Span = 2.26
Mid_Panel_Span   = 2.26
Outer_Panel_Span = 2.64
MC_AR          = Wingspan / mean([Root_Chord, Mid_Chord_1, Mid_Chord_2, Tip_Chord])
Area           = abs((parse_path("M 0,-7023.0001 H 17.000001 37 48 l -7,-88.5 -7,-90.5 -6.583193,-84.0101 "+
                             "c -1.570448,-20.0409 1.512123,-19.4597 1.512123,-19.4597 0,0 " + 
                             "-6.052764,-1.5262 -9.720819,-0.6646 -7.250914,1.7032 -7.285934,8.1032 -8.213607,20.1058 " + 
                             "L 2.5,-7202.0001 l -2.5,90 v 89").area()*2)/1550.0)

# TODO: these have different units than the Area above, only good for doing the proportion of each panel.  Need to fix
Inner_Area     =  abs((parse_path("M 0 20256 L 0 28800 L 1632 28800 L 3552 28800 L 4608 28800 L 3936 20256 L 0 20256 z ").area()*2)/1550.0)
Middle_Area    =  abs((parse_path("M 240 11616.01 L 0 20256 L 0 20256.02 L 3936.002 20256.02 L 3936 20256 L 3264 11616.01 L 240 11616.01 z ").area()*2)/1550.0)

       
Outer_Area     =  abs((parse_path("M 2099.4512 1593.791 C 2008.9912 1593.8798 1921.0077 1601.0041 1843.9785 1619.0977 " +
                                  "C 1147.8908 1782.6049 1144.5293 2397.0043 1055.4727 3549.2539 L 240 11616 L 3264 11616 " +
                                  "L 2632.0137 3551.0312 C 2481.2507 1627.1049 2777.1777 1682.8984 2777.1777 1682.8984 " +
                                  "C 2777.1777 1682.8984 2422.5226 1593.4739 2099.4512 1593.791 z ").area()*2)/1550.0)

AR             = (Wingspan**2) / Area
Wing_Loading   = TOW / Area


Area2 = Inner_Area+Middle_Area+Outer_Area
Inner_Contribution = Inner_Area/Area2
Middle_Contribution = Middle_Area/Area2
Outer_Contribution = Outer_Area/Area2

# partial areas for airfoils
A1_Area =  ((Root_Chord + ((Root_Chord + Mid_Chord_2)/2.0))/2.0) * Inner_Panel_Span
A2_Area =  ((Mid_Chord_2 + ((Root_Chord + Mid_Chord_2)/2.0))/2.0) * Mid_Panel_Span
A2_Area += ((Mid_Chord_2 + ((Mid_Chord_2 + Tip_Chord)/2.0))/2.0) * (Outer_Panel_Span/2.0)
A3_Area =  ((Tip_Chord + ((Mid_Chord_2 + Tip_Chord)/2.0))/2.0) * (Outer_Panel_Span/2.0)
A1_Coefficient = (2.0*A1_Area)/Area
A2_Coefficient = (2.0*A2_Area)/Area
A3_Coefficient = (2.0*A3_Area)/Area

print("Mean Chord Aspect Ratio        = " + str(MC_AR))
print("Wing Area Aspect Ratio         = " + str(AR))
print("Wing Area                      = " + str(Area))
print("Wing Inner Area                = " + str(Inner_Area))
print("Wing Middle Area                = " + str(Middle_Area))
print("Wing Outer Area                = " + str(Outer_Area))
print("Wing Loading                   = " + str(Wing_Loading))
print("Airfoil 1 Area                 = " + str(A1_Area))
print("Airfoil 2 Area                 = " + str(A2_Area))
print("Airfoil 3 Area                 = " + str(A3_Area))
print("Airfoil 1 Coefficient          = " + str(A1_Coefficient))
print("Airfoil 2 Coefficient          = " + str(A2_Coefficient))
print("Airfoil 3 Coefficient          = " + str(A3_Coefficient))
print("x = " + str((Inner_Area+Middle_Area+Outer_Area)/Area))
Cl = 0.7
Cd = 0.2
Efficiency = Cl/Cd


# fuselage
Fuselage_Width = 25.0  #inches
Fuselage_Frontal_Area = ( (6 * Fuselage_Width) + 
                          (pi * (Fuselage_Width/2.0) * 13)/2.0 + 
                          (pi * (Fuselage_Width/2.0) * 16) ) / 1550.0 # square meters
Fuselage_Drag_Coefficient = 0.045 # (Wild Ass Guess from Stelio Frati's book
Fuselage_Drag             = Fuselage_Drag_Coefficient * (Fuselage_Frontal_Area / Wingspan)

print("Fuselage Frontal Area         = " + str(Fuselage_Frontal_Area))
print("Fuselage Drag Coefficient     = " + str(Fuselage_Drag_Coefficient))
print("Fuselage Drag                 = " + str(Fuselage_Drag))



# tail
Horizontal_Tail_Half_Area      = 670.82
Horizontal_Tail_Area           = 670.82 * 2.0
Vertical_Tail_Area             = 1870.74

Empennage Area                 = Horizontal_Tail_Area + Vertical_Tail_Area
