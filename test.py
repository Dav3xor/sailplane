from flat_wrap import *
import math

e        = [{'vertical_center': 0, 'horizontal_center': 0, 'width': 5, 'height':15, 'datum': 0, 'amount': 0.5},
            {'vertical_center': 0, 'horizontal_center': 0, 'width': 5, 'height':5, 'datum': 1, 'amount': 0.5}]
a = make_ellipse(e[0])
b = make_ellipse(e[1])
#print(a)
#print(b)

numsteps=100
step_angle = (2*3.14159*e[0]['amount'])/(numsteps-1)

for j in range(5):
    c=[b[0]]
    for i in range(len(a)-1):
        cur_angle = i*step_angle
        aa = math.atan2(a[i][1]-a[i+1][1], a[i][2]-a[i+1][2])
        ab = math.atan2(b[i][1]-b[i+1][1], b[i][2]-b[i+1][2])
        b2 = b[i+1]
        difference = (aa-ab)/80
        c.append(ellipse_point(cur_angle+difference,e[1]))

        ac = math.atan2(b[i][1]-b[i+1][1], b[i][2]-b[i+1][2])
        #print(f'aa={aa} bb={ab} aa-ab={aa-ab} ac={ac} b2={b2} b[i+1]={b[i+1]}')
        print(f'{cur_angle} {aa} {ab} {difference}')
    print('---')
    c[-1]=b[-1]
    for i in range(len(a)-1):
        aa = math.atan2(a[i][1]-a[i+1][1], a[i][2]-a[i+1][2])
        ab = math.atan2(b[i][1]-b[i+1][1], b[i][2]-b[i+1][2])
        ac = math.atan2(c[i][1]-c[i+1][1], c[i][2]-c[i+1][2])
        #print(f'{a[i]} {b[i]} {c[i]}')
        #print(f'{aa} {ab} {ac}')
    b = c 
#ellipses(e)

