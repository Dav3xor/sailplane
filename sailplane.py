from statistics import mean
from math import sqrt, pi


# airfoils to try:  NACA 633-618
#                   NACA 652-415
#                   SM701
#                   UAG 88-143/20
#                   Selig S8052

# this omits the base, for wetted area estimation
def cone_surface_area (r,l):
    return pi*r*l
    
def trapezoid_area(root, tip, length):
    return ((root+tip) * length / 2)

def itom(inches):
    return inches * 0.0254

def kgsmlbft(kgsm):
    return kgsm * .2048

def prt(name, value):
    print(f"{name.ljust(40)} = {value}")


tau            = 2*pi

class Airfoil:
    def load_data(self,filename):
        cur_polar = {}
        with open(filename,'r') as infile:
            for line in infile:
                if line.startswith('BIGFOIL'):
                    if cur_polar:
                        print("xxx")
                        self.polars[cur_polar['Re']] = cur_polar
                        cur_polar = {}
                elif 'Cl Max:' in line:
                    data = line.split(':')[1]
                    cur_polar['ClMax'] = float(data.strip().split('\t')[0])
                    data = line.split('=')[1]
                    cur_polar['ClMaxAlpha'] = float(data.strip().split('\t')[0])
                elif 'L/D Max:' in line:
                    data = line.split(':')[1]
                    cur_polar['LDMax'] = float(data.strip().split('\t')[0])
                    data = line.split('=')[1]
                    cur_polar['LDMaxAlpha'] = float(data.strip().split('\t')[0])
                elif 'Re:' in line:
                    data = line.split('\t')
                    cur_polar['Re']    = int(data[1])
                    cur_polar['CdMin'] = float(data[5])
                    cur_polar['CdMinAlpha'] = float(data[7])
                elif 'Mach:' in line:
                    data = line.split('\t')
                    cur_polar['Cl'] = []
                    cur_polar['Mach']      = float(data[1])
                    cur_polar['Cl'].append((0,float(data[5])))
                elif '@' in line:
                    data = line.split('\t')
                    cur_polar['Cl'].append((float(data[4].split('=')[1][0:3]), float(data[5])))
                    print(data)
                elif 'alpha' in line:
                    pass
                elif line == '\n':
                    print ("empty")
                else:
                    try:
                        data = line.split('\t')[:5]
                        key = data[0]
                        data = list(map(float,data))
                        if 'data' not in cur_polar:
                            cur_polar['data'] = {}
                        cur_polar[key] = {'Cl': data[1], 
                                          'Cd': data[2], 
                                          'Cm': data[3], 
                                          'LD': data[4]}
                    except:
                        pass

            if cur_polar:
                self.polars[cur_polar['Re']] = cur_polar
            print(self.polars.keys())        
            #print (self.polars)
            #print (self.ClMax)
            #print (self.ClMaxAlpha)
            #print (self.LDMax)
            #print (self.LDMaxAlpha)
    def __init__(self, filename):
        self.polars = {}
        self.load_data(filename)

# assume metric *inside* of classes...
class Fin:
    def __init__(self, root_chord, tip_chord, single_span):
        self.root_chord     = root_chord
        self.tip_chord      = tip_chord
        self.single_span    = single_span
class Wing(Fin):
    def __init__(self, wingspan, root_chord, tip_chord, single_span):
        Fin.__init__(self, root_chord, tip_chord, single_span)
        self.wingspan         = wingspan
        self.taper_ratio      = self.tip_chord / self.root_chord
        self.mac              = (2/3)*self.root_chord*((1+self.taper_ratio+(self.taper_ratio**2)) / (1+self.taper_ratio))
        self.single_wing_area = trapezoid_area(self.root_chord, self.tip_chord, self.single_span)
        self.wetted_area      = (self.single_wing_area * 4) * 1.2

    def set_reference_area(self, fuselage):
        # trapezoid area of 2 wings + projected area through fuselage
        self.sref           = (self.single_wing_area * 2) + (fuselage.width * self.root_chord)
        # Wing area that has flaps (TODO: approximation, get more precise later)
        self.flapped_area  = self.sref * 0.8
        
        # TODO: get these from Airfoil...
        self.aoa_zero_lift = -4.0   #40A615
        self.ideal_clmax   = 1.673  
        self.clmax         = 0.9*self.ideal_clmax
        self.clmax25       = 2.386             # 25% flap at 25%
        self.clmaxflapped   = self.clmax + (0.9*(self.clmax25-self.clmax)*(wing.flapped_area/self.sref))

        self.ar             = (self.wingspan**2) / self.sref
        self.wing_loading   = airplane.tow / self.sref

airfoil20 = Airfoil('GA-40A620.txt')

class Fuselage:
    def __init__(self, width, drag_coefficient):
        self.width = width
        self.drag_coefficient = drag_coefficient

    def set_frontal_area(self, frontal_area, wing):
        self.frontal_area = frontal_area
        self.drag         = self.drag_coefficient * (self.frontal_area / wing.wingspan)

class Airplane:
    def __init__(self, empty_weight, pilot_weight, payload_weight):
        self.empty_weight   = empty_weight
        self.pilot_weight   = pilot_weight
        self.payload_weight = payload_weight
        self.tow            = self.empty_weight + self.pilot_weight + self.payload_weight

class VerticalTail(Fin):
    pass

class Atmosphere:
    def __init__(self, p, velocity): #knots
        self.p        = p
        self.velocity = velocity
        self.q        = .5*self.p*((self.velocity*1.689)**2) # convert to feet per second...)


atmosphere = Atmosphere(0.00211, 60)

# 4000ft, standard day...
p = 0.00211
V = 60       # knots
q = .5*p*((V*1.689)**2) # convert to feet per second...)
airplane = Airplane(empty_weight   = 180.0, 
                    pilot_weight   = 120.0, 
                    payload_weight = 5.0)

wing     = Wing(wingspan    = itom(590.5),
                root_chord  = itom(48),
                tip_chord   = itom(14),
                single_span = itom(284))
print("")
print("Fuselage")
print("-"*80)
# fuselage
# Fuselage_Width = itom(25.0)  #inches
# TODO: I've changed these


fuselage = Fuselage(width            = itom(25.0), 
                    drag_coefficient = 0.045)

fuselage.set_frontal_area((itom(6) * fuselage.width) + 
                          (pi * (fuselage.width/2.0) * itom(13))/2.0 + 
                          (pi * (fuselage.width/2.0) * itom(16)), wing ) # square meters


prt("Fuselage Frontal Area",fuselage.frontal_area)
prt("Fuselage Drag Coefficient",fuselage.drag_coefficient)
prt("Fuselage Drag",fuselage.drag)





print("")
print("Wings")
print("-"*80)
# wings

# current airfoil pick -- Riblett 

# AoA    Clmax          Name
# 10.5   1.479          40A612
# 13     1.673          40A615
# 16.5   1.954          40A620





wing.set_reference_area(fuselage)

prt("Root Chord", wing.root_chord)
prt("Tip Chord",  wing.tip_chord)




prt("Single Wing Area",wing.single_wing_area)
prt("Sref (reference wing area)",wing.sref)
prt("Swet (wing wetted area)",wing.wetted_area)
prt("Sflapped (wing wetted area)",wing.flapped_area)
prt("Clmax",wing.clmax)
prt("Clmax, flaps 25%", wing.clmaxflapped)




prt("Aspect Ratio",wing.ar)
prt("Reference Wing Area (Sref)",wing.sref)
prt("Wing Loading",wing.wing_loading)

Cl = 0.7
Cd = 0.2
Efficiency = Cl/Cd



print("")
print("Tail")
print("-"*80)



htail    = Wing(wingspan    = itom(62*2),
                root_chord  = itom(25),
                tip_chord   = itom(18),
                single_span = itom(62))


# tail
# TODO: probably changed these too
HTail_Root_Chord     = 25
HTail_Tip_Chord      = 18
HTail_Single_Span    = 62 

htail.half_area      = trapezoid_area(htail.root_chord, htail.tip_chord, htail.single_span)
htail.area           = htail.half_area * 2.0
htail.wet_area       = htail.area * 1.1

VTail_Area           = 1870.74 / 1550.0
VTail_Wet_Area       = VTail_Area * 2.2

Empennage_Area       = htail.area + VTail_Area
Empennage_Wet_Area   = htail.wet_area + VTail_Wet_Area
prt("HTail Half Area",htail.half_area)
prt("HTail Area",htail.area)
prt("HTail Wet Area",htail.wet_area)
prt("Vtail_Area",VTail_Area)
prt("Vtait Wet Area",VTail_Wet_Area)
prt("Empennage Area",Empennage_Area)
prt("Empennage Wet Area",Empennage_Wet_Area)






# wetted area approximation
# this is an approximation!

print("")
print("wetted area approximation:")
print("-"*80)

fuselage_radius      = fuselage.width / 2.0

# tailcone -- basically a cone and two rectangles
tailcone_length      = 151
tailcone_side_height = 9
tailcone_side_length = sqrt((tailcone_length**2)+(fuselage_radius**2))
Tailcone_Cone_Area   = cone_surface_area(fuselage_radius, tailcone_length) / 1550.0
Tailcone_Sides_Area  = ( tailcone_side_height*tailcone_side_length*2 ) / 1550.0
Tailcone_Area        = Tailcone_Cone_Area + (Tailcone_Sides_Area)

prt("Tailcone Cone Area",Tailcone_Cone_Area)
prt("Tailcone Sides Area",Tailcone_Sides_Area)
prt("Tailcone Surface Area",Tailcone_Area)

# mid fuselage -- a cylinder and 2 parallel rectangles
mid_length           = 31.0
Mid_Cylinder_Area    = ((2*pi*fuselage_radius)*mid_length) / 1550.0
Mid_Sides_Area       = ((mid_length*(tailcone_side_height+2))*2) / 1550.0
Mid_Area             = Mid_Cylinder_Area + Mid_Sides_Area

prt("Mid Top/Bottom Area",Mid_Cylinder_Area)
prt("Mid Sides",Mid_Sides_Area)
prt("Mid Fuselage Area",Mid_Area)

# nose -- a more wild ass guess
upper_nose_length    = 46
lower_nose_length    = 72

Nose_Top_Cone        = (cone_surface_area(fuselage_radius, upper_nose_length) / 1550.0) / 2.0
Nose_Bottom_Cone     = (cone_surface_area(fuselage_radius, lower_nose_length) / 1550.0) / 2.0
Nose_Sides           = (40*9*2) / 1550.0
Nose_Area            = Nose_Top_Cone + Nose_Bottom_Cone + Nose_Sides

prt("Nose Top Cone",Nose_Top_Cone)
prt("Nose Bottom Cone",Nose_Bottom_Cone)
prt("Nose Sides",Nose_Sides)



Fuselage_Wet_Area    = Nose_Area + Mid_Area + Tailcone_Area
prt("Fuselage Wet Area",Fuselage_Wet_Area)




# estimated who1e aircraft wetted area
Wetted_Area = wing.wetted_area + Empennage_Wet_Area + Fuselage_Wet_Area
prt("Whole Wet Area",Wetted_Area)




print("")
print("Aero")
print("-"*80)

# Simple induced drag (Raymer 'drag due to lift' p. 18)
K = 1 / (.75*pi*wing.ar)

prt("Induced Drag",K)

#Equivalent Skin Friction Coefficient, Raymer p. 18
#Cfe = .0038
Cfe = .0045

#Parasitic Drag Coefficient ... p. 17
Cdo = Cfe*(wing.wetted_area/wing.sref)
prt("Parasitic Drag Coef",Cdo)

# L/D


Wing_Loading_lbs = kgsmlbft(wing.wing_loading)
LoverD =  1.0 / ( ((q*Cdo)/Wing_Loading_lbs) + (Wing_Loading_lbs * (K/q)) )
prt("L/D",LoverD)



prt("Taper Ratio",wing.taper_ratio)
prt("MAC",wing.mac)


Cruise_Lift_Coefficient = Wing_Loading_lbs / V
Cruise_AoA = Cruise_Lift_Coefficient*(10+(18/wing.ar)) + wing.aoa_zero_lift
prt("Cruise Lift Coefficient",Cruise_Lift_Coefficient)
prt("Cruise AoA",Cruise_AoA)


# Tail sizing...
Cht                  = .6  # a little higher than Raymer's high value, big wing, lots of Cm, etc...
Cvt                  = .04 # a little higher than Raymer's high value, big wing, lots of Cm, etc...
Lht                  = itom(142.0) # length between wing and horizontal tail MAC
Lvt                  = itom(161.0) #    "      "     "    "  vertical   tail MAC
HTail_Sizing         = Cht * ((wing.mac*(wing.sref))/Lht)
VTail_Sizing         = Cvt * ((15.0*(wing.wingspan/2.0))/Lvt)
prt("HTail_Sizing calc-actual",f"{HTail_Sizing}-{HTail_Area}")
prt("VTail_Sizing calc-actual",f"{VTail_Sizing}-{VTail_Area}")


