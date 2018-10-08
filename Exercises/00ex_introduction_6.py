import numpy as np
def square(x):
    try:
        return x**2
    except:
        print("Error")
        return 0

def cubic(x):
    try:
        return x**3
    except:
        print("Error")
        return 0
x = 10*np.random.rand();
print("x=", x)
print("x^6=", cubic(square(x)))
