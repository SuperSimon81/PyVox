
import matplotlib.pyplot as plt
import math
import time





def draw_poly(level,angle,div,fill_color):
    print(level,angle)
    divisions = div[level]
    
    a=level-1 
    b=level-1
    #APOTHEM
    if not div[level]==div[level-1]:
        if angle % 2 == 0:
            a = (level-1)*math.cos(math.pi/(divisions/2))
        else:
            b = (level-1)*math.cos(math.pi/(divisions/2))
    else:
        a=level-1 
        b=level-1
    x1 = level*math.sin(2*math.pi*angle/divisions) #top left
    x2 = level*math.sin(2*math.pi*(angle+1)/divisions) #top right
    x3 = (b)*math.sin(2*math.pi*angle/divisions) #bottom left
    x4 = (a)*math.sin(2*math.pi*(angle+1)/divisions) #bottom right

    y1 = level*math.cos(2*math.pi*angle/divisions)
    y2 = level*math.cos(2*math.pi*(angle+1)/divisions)
    y3 = (b)*math.cos(2*math.pi*angle/divisions)
    y4 = (a)*math.cos(2*math.pi*(angle+1)/divisions)
    
    points=[[x1,y1],[x2,y2],[x4,y4],[x3,y3]]
    line = plt.Polygon(points, closed=True, fill=fill_color, edgecolor='b')
    return line

def get_neighbours(level,angle,div):
    list=[]
    #Down
    if div[level]==div[level-1]:
        list.append([level-1,angle])
    else:
        list.append([level-1,math.floor(angle/2)])
    #Up    
    if div[level]==div[level+1]:
        list.append([level+1,angle])
    else:
        list.append([level+1,(angle*2)+1])
        list.append([level+1,angle*2])
    #Left
    list.append([level,(angle-1)%div[level]])
    #Right
    list.append([level,(angle+1)%div[level]])
    return list

def draw_neighbours(level,angle,div):
    polys = []
    neighbours = get_neighbours(level,angle,div)
    for item in neighbours:
        polys.append(draw_poly(item[0],item[1],div,'b'))
    
    #polys.append(draw_poly(level,angle,div,'black'))
    
    return polys



    
    



plt.axes( )


#points = [[2, 1], [8, 1], [8, 4]]
#polygon = plt.Polygon(points)


edges =4
shapes = 10
points=[]
r=1.1
inc=-0.01
count=1
radius=1
divisions = []
counter=0
test    = [0,1,2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17]
divisions=[1,2,8,16,16,32,32,32,32,64,64,64,64,64,64,64,64,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256,256]

#divisions.append(int(edges/2))
for poly in range(1,shapes):
    last_points = points
    points=[]
    lines = []
    radius = 1*count
    circ=2*math.pi*radius
    segment = circ/edges
     
    
    if segment > math.pi/2:
        edges *=2
        
        counter +=1
   
    #divisions.append(int(edges/2))
    for edge in range(edges):
        #radius=(r*count)
        a = (radius-1)*math.cos(math.pi/(edges/2))
        points.append([radius*math.sin(2*math.pi*edge/edges),radius*math.cos(2*math.pi*edge/edges)])
        
        plt.plot([(a)*math.sin(2*math.pi*edge/edges),(radius)*math.sin(2*math.pi*edge/edges)],[(a)*math.cos(2*math.pi*edge/edges),(radius)*math.cos(2*math.pi*edge/edges)], 'k-', lw=0.5)

    line = plt.Polygon(points, closed=True, fill=None, edgecolor='r')
    
    plt.gca().add_line(line)
    #plt.gca().add_line(points+last_points)
    count += 1
    #r += inc



#for n in range(10):  
    #filled=draw_poly(n,0,divisions)
    #plt.gca().add_line(filled)

polys = draw_neighbours(4,12,divisions)
for line in polys:
    pass
    plt.gca().add_line(line)
    

#test = draw_poly(5,0,divisions,'r')
#plt.gca().add_line(test)
plt.axis('scaled')
#print(divisions)

plt.show()
