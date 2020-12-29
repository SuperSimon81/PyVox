
import matplotlib.pyplot as plt
import math
import cmath



def S(z,rp):
    return rp*cmath.exp(z) 




plt.axes( )


rp=0.1
pass
cnums = []
cnums2 = []
#points = [[2, 1], [8, 1], [8, 4]]
#polygon = plt.Polygon(points)
for x in range(-100,100):
    for y in range(-100,100):
        cnums.append(complex(x,y))

for c in cnums:
    cnums2.append(S(c,rp))

X = [x.real for x in cnums2]
Y = [x.imag for x in cnums2]

plt.scatter(X,Y, color='red')
#line = plt.Polygon(points, closed=True, fill=None, edgecolor='r')

#plt.gca().add_line(line)
#plt.gca().add_line(points+last_points)
   
        

plt.axis('scaled')
plt.show()