
import matplotlib.pyplot as plt
import math
import cmath



def S(z,rp):
    return rp*math.e**z 




plt.axes( )


rp=0.1
pass
cnums = []
cnums2 = []
#points = [[2, 1], [8, 1], [8, 4]]
#polygon = plt.Polygon(points)
points = []
cpoints = []
for x in range(0,11):
    points.append([complex(x,10),complex(x,10)])
    points.append([complex(0,x),complex(10,x)])
    cpoints.append([S(complex(x,0),2), S(complex(x,10),2)])
    cpoints.append([S(complex(0,x),2), S(complex(10,x),2)])
    
for p in points:
    plt.plot([p[0].real,p[1].real],[p[0].imag,p[1].imag])

    

for p in cpoints:
    pass
    plt.plot([p[0].real,p[1].real],[p[0].imag,p[1].imag])






#line = plt.Polygon(cnums2, closed=True, fill=None, edgecolor='r')

#plt.gca().add_line(line)
#plt.gca().add_line(points+last_points)
   
        

plt.axis('scaled')
plt.show()