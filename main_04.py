#
#
# Esercitazione Lezione 4
#
#

import math


from IPython.display import Image
Image(url='http://www.dspguide.com/graphics/F_4_2.gif')

print(1/10)
print(0.1)
print(0.1 == 1/10)
print(0.1 + 0.1 + 0.1 == 0.3)


for e in [14,15,16]: print (7+1.0*10**-e)
print (format(math.pi, '.13f'))  # give 13 significant digits
print ('%.15f' % (0.1 * 0.1 * 100)) # give 15 significant digits

# now repeat trying with >15 digits!


print (format(math.pi, '.13f'))  # give 13 significant digits
print ( '%.17f' % (0.1 * 0.1 * 100)  ) # give 15 significant digits

# nota: con round perdiamo quello che c'e` dietro alla prima cifra decimale
# quindi cosi` resta 1.000000, senno` nel caso precedente
# aggiungeva un 22 alla fine delle 15 cifre, cioe` la 17 e 18
# erano 22
print (format(math.pi, '.13f'))  # give 13 significant digits
print ( '%.17f' % round((0.1 * 0.1 * 100))  ) # give 15 significant digits

import numpy as np
probs = np.random.random(1000)
print (np.prod(probs))

# when multiplying lots of small numbers, work in log space
print (np.sum(np.log(probs)))


x1 = 1.57078
x2 = 1.57079
t1 = math.tan(x1)
t2 = math.tan(x2)

print ('t1 =', t1)
print ('t2 =', t2)
print ('% change in x =', 100.0*(x2-x1)/x1)
print ('% change in tan(x) =', (100.0*(t2-t1)/t1))


import numpy as np
import matplotlib.pyplot as plt

#% matplotlib inline

def f(x):
    return (1 - np.cos(x))/(x*x)

x = np.linspace(-4e-8, 4e-8, 100)
plt.plot(x,f(x));
plt.axvline(1.1e-8, color='red')
plt.xlim([-4e-8, 4e-8]);

plt.show()


# sum of squares method (vectorized version)
# watch out! big number minus big number!
def sum_of_squers_var(x):
    n = len(x)
    return (1.0/(n*(n-1))*(n*np.sum(x**2) - (np.sum(x))**2))

# direct method
# squaring occuring after subtraction
def direct_var(x):
    n = len(x)
    xbar = np.mean(x)
    return 1.0/(n-1)*np.sum((x - xbar)**2)


# Welford's method
# an optimized method
def welford_var(x):
    s = 0
    m = x[0]
    for i in range(1, len(x)):
        m += (x[i]-m)/i
        s += (x[i]-m)**2
    return s/(len(x) -1 )



x_ = np.random.uniform(0,1,int(1e3))
x = 1e12 + x_

# correct answer
print (np.var(x_))

print (sum_of_squers_var(x))
print (direct_var(x))
print (welford_var(x))



