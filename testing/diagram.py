
import matplotlib.pyplot as plt
import math


plt.axes( )


#points = [[2, 1], [8, 1], [8, 4]]
#polygon = plt.Polygon(points)

points=[]
r =4

points=[]
for i in range(r):
    points.append([math.sin(2*math.pi*i/r),math.cos(2*math.pi*i/r)])
line = plt.Polygon(points, closed=True, fill=None, edgecolor='r')
plt.gca().add_line(line)
r *=2
points=[]
for i in range(r):
    points.append([2*math.sin((2*math.pi*i/r)),2*math.cos(2*math.pi*i/r)])
line = plt.Polygon(points, closed=True, fill=None, edgecolor='r')
plt.gca().add_line(line)

line = plt.Line2D((0,0), (2,1),color='b')
plt.gca().add_line(line)
line = plt.Line2D((0,0), (-2,-1),color='b')

plt.gca().add_line(line)
plt.axis('scaled')
plt.show()