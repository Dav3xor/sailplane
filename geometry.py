import math


class Polygon:
    def __init__(self, points=[],color='black',dash=None, tx=0,ty=0,closed=True):
        self.points = points.copy()
        self.closed = True
        self.colorx  = color
        self.dash   = dash
    def copy(self):
        return Polygon(self.points.copy())
    def translate(self,tx,ty):
        self.points =  [tuple([point[0]+tx, point[1]+ty] + list(point[2:])) for point in self.points]
        return self

    def reverse(self):
        self.points.reverse()

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        self.points[key] = value

    def __add__(self, other):
        if type(other) in [list,tuple]:
            return Polygon(self.points+list(other))
        elif type(other) == Polygon:
            return Polygon(self.points+other.points)
        else:
            raise Exception

    def __len__(self):
        return len(self.points)

    def __repr__(self):
        poly = ''
        for point in self.points:
            try:
                poly += f'{point[0]},{point[1]} \n'
            except:
                print(self.points)
                5/0
        if self.dash:
            dash = f"stroke-dasharray='{self.dash}'" # svg format --> 0.5, 0.5
        else:
            dash = ''

        if self.closed:
            return f'<polygon stroke-width="0.1" fill="none" stroke="{self.colorx}" points="{poly}" />'
        else:
            return f'<polyline stroke-width="0.1" {dash} fill="none" stroke="{self.colorx}" points="{poly}" />'

    def mirrorz(self):
        points2 = []
        for i in self.points:
            points2.append(i)
            points2.append((i[0],i[1],i[2]*-1.0))
        return points2

    def append(self,point):
        self.points.append(point)
   
   
    def color(self, color):
        self.colorx = color
        return self

    def reduce2d(self,xindex,yindex):
        self.points = [(i[xindex],i[yindex]) for i in self.points]
        return self

    def prepend(self,point):
        self.points = [point] + self.points

    def insert(self,loc,data):
        self.points.insert(loc,data)

def parallel(a,b):
    p = Polygon()
    for i in range(max(len(a),len(b))):
        if i < len(a):
            p.append(a[i])
        if i < len(b):
            p.append(b[i])
    return p

def distance(a,b):
    if len(a) != len(b):
        5/0
    if len(a) == 3:
        return distance3(a[0]-b[0], a[1]-b[1],a[2]-b[2])
    if len(a) == 2:
        return distance2(a[0]-b[0], a[1]-b[1])
def distance3(dx,dy,dz):
    return math.sqrt(dx**2 + dy**2 + dz**2)

def distance2(dx,dy):
    return math.sqrt(dx**2 + dy**2)

    
# trilateration:
# https://github.com/noomrevlis/trilateration/blob/master/trilateration2D.py
def get_intersections(p1, r1, p2, r2):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    #d=math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
    d = distance(p2,p1)

    # non intersecting
    if d > r1 + r2 :
        print("non intersecting")
        return None
    # One circle within other
    if d < abs(r1-r2):
        print(f"within d={d} r1={r1} r2={r2}")
        return None
    # coincident circles
    if d == 0 and r1 == r2:
        print("coincident")
        return None
    else:
        a = (pow(r1, 2) - pow(r2, 2) + pow(d, 2)) / (2*d)
        h  = math.sqrt(pow(r1, 2) - pow(a, 2))
        x0 = p1[0] + a*(p2[0] - p1[0])/d 
        y0 = p1[1] + a*(p2[1] - p1[1])/d
        rx = -(p2[1] - p1[1]) * (h/d)
        ry = -(p2[0] - p1[0]) * (h / d)
        return ((x0+rx, y0-ry), (x0-rx, y0+ry))

def isleft(a, b, c):
  return (b[0] - a[0])*(c[1] - a[1]) - (b[1] - a[1])*(c[0] - a[0]) > 0;
  return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x) > 0;

def find_pointl(a,b,A,B):
    points = get_intersections(a,A,b,B)
    if points:
        return points[0] if isleft(a,b,points[0]) else points[1]
    else:
        print("?")
        5/0

def find_pointr(a,b,A,B):
    points = get_intersections(a,A,b,B)
    if points:
        return points[1] if isleft(a,b,points[0]) else points[0]
    else:
        print("?")
        5/0

def quarter_round(radius,zangle=0):
    a = []
    for i in range(10):
        angle = (90/10*i)*2*3.14159/360
        x=0
        y=math.cos(angle)*radius
        z=math.sin(angle)*radius
        a.append((x,y,z))
    return a
def rotatez(points, angle):
    rotated = []
    for point in points:
        newpoint = (point[0]*math.cos(angle) - point[1]*math.sin(angle),
                    point[0]*math.sin(angle) + point[1]*math.cos(angle),
                    point[2])
        rotated.append(newpoint)     
    return rotated
def ellipse_point(angle, e):
    x = math.sin(angle)*e['height']
    y = math.cos(angle)*e['width']
    return 0,x,y

def make_unit_ellipse(e, numsteps = 100, flip=False, mode=1):
    points = Polygon()
    flip = -1.0 if flip else 1.0
    step_angle = (math.tau*e['amount'])/(numsteps-1)
    for step in range(numsteps):
        angle = step * step_angle
        if mode == 1:
            points.append(( 0,
                            (math.sin(angle)*e['height']*flip),
                            (math.cos(angle)*e['width'])))
        if mode == 2:
            points.append(( (math.sin(angle)*e['height']*flip),
                            0,
                            (math.cos(angle)*e['width'])))
        if mode == 3:
            points.append(( (math.sin(angle)*e['height']*flip),
                            (math.cos(angle)*e['width'])))
    return points

def make_ellipse(e, numsteps=100, flip=False, mode=1):
    ellipse = make_unit_ellipse(e,numsteps,flip,mode)
    translate_poly(ellipse, e['datum'], e['vertical_center'], e['horizontal_center'])
    return ellipse

def translate_point(p, x, y, z):
    return (p[0]+x, p[1]+y, p[2]+z)
def translate_poly(p, x, y, z):
    for i in range(len(p)):
        p[i] = translate_point(p[i],x,y,z)


def points_to_circles(points, radius, width = '.1', units = ''):
    output = ''
    for point in points:
        output += f'<circle r="{radius}{units}" cx="{point[0]}{units}" cy="{point[1]}{units}"  stroke="black" stroke-width="{width}{units}" fill="none" />\n'
    return output


def points_to_line(p1,p2):
    return f'<line x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}" style="stroke:black;stroke-width:0.1" />'
