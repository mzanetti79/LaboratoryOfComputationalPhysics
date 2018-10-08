import math

def normalize(vec):
    try:
        norm = 0
        for i in range(0,len(vec)):
            norm += vec[i]**2
        norm = math.sqrt(norm)
        for i in range(0,len(vec)):
            vec[i] = vec[i]/norm
        return vec
    except:
        print("Error")
        return 0

print(normalize([0,1,1]))
