import math

def distance2d(u,v):
    try:
        dist = 0;
        for i in range(0,len(u)):
            dx = u[i]-v[i]
            dist += dx*dx
        return math.sqrt(dist)
    except:
        print("Error")
        return 0
    
print(distance2d((3,0),(3,5)))
