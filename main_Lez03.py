# even the heaven shall burn as we gather
# Lezione 03
# LaboratoryOfComputationalPhysics

# ---- I C E _ B R E A K I N G _ S M A L L T A L K -------------

print("Blyat")
import time
from math import pi
from scipy.constants import g

# --------------------------------------------------------------

print("\n\nEs 1\n")
# Es 1.1 -------------------------------------------------------

print("Es 1.1\n")
start = time.time()
ans = []
for i in range(3):
    for j in range(4):
        ans.append((i, j))
    #enddo
#enddo
finish = time.time()

print("For espliciti: \n", ans, "\nin ", finish-start, " s.")

start = time.time()
ans = [(i, j) for i in range(3) for j in range(4)]
finish = time.time()

print("List comprehension: \n", ans, "\nin ", finish-start, " s.")


# Es 1.2 -----------------------------
print("\n\nEs 1.2\n")

ans = map(lambda x: x*x , filter(lambda x: x % 2 == 0, range(5)))
print(list(ans))

ansia = []
for x in range(5):
    if x % 2 == 0:
        ansia.append(x**2)
    #endif
#enddo
print(ansia)

print("\n\nAncora un esperimento\n\n")

def Blyat(x):
    return x + 3
#enddef

trial = [i for i in range(20)]
print(trial)
ris = map(Blyat, trial)
print(list(ris))


# se volessimo metterci un filtro?
# quella della sigaretta che mi fumo oraaaa ==== ???


# qui torna molto molto comoda la lambda
ris = map(Blyat, filter(lambda n : n % 2 == 0 , trial))
print(list(ris))
'''
ris = map(Blyat, filter(lambda n : n % 2 == 0 , lambda x : x + 3 for x in trial))
print(list(ris))
nice try whatsoever
'''


# Es 2 ---------------------------------------------
print("\n\nEs 2\n")

x = 5
def f(alist):
    for i in range(x):
        alist.append(i)
    return alist

alist = [1,2,3]
ans = f(alist)
print("Trial 1\n")
print (ans)
print (alist) 

def ff(alist,n):
    listToModify = []
    for i in range(len(alist)):
        listToModify.append(alist[i])
    #enddo
    for i in range(n):
        listToModify.append(i)
    #enddo
    return listToModify
#enddef

adahList = [2,3,4]
ansya = ff(adahList,x)
print("Trial 2\n")
print(ansya)
print(adahList)


# Es 3 ------------------------------------------------------
print("\n\nEs 3\n")

def DecoratorToSayHello(square):
    def wrapper(x):
        print("Oltre a restituire il quadrato, la funzione square dice HELLO")
        print("Chiamata di square in wrapper: ", square(x))
    #enddef
    return wrapper
#enddef


@DecoratorToSayHello
def square(x):
    ris = x**2
    return ris
#enddef

# NOTA: questo blocco appena scritto serve per non dover scrivere
# tipo:
#	square = DecoratorToSayHello(square)
# cioe` l'effetto e` comunque che puntiamo al blocco wrapper

x = 3
print(square(x))


# Es 4 -----------------------------------------------------
print("\n\nEs 4\n")

def factorial(n):
    if n > 1:
        ris = n * factorial(n-1)
        return ris
    elif n <= 1:
        return 1
    #endif
#enddef

def factorialNoRecursive(n):
    if n > 1:
        ris = 1
        for i in range(1,n+1):
            ris *= i
        #enddo
        return ris
    elif n <= 1:
        return 1
    #endif
#enddef

n = 4
start = time.time()
ris1 = factorial(n)
finish = time.time()
print("Fattoriale di ", n, ": ", ris1, " in ", finish-start, " s.")

start = time.time()
ris2 = factorialNoRecursive(n)
finish = time.time()
print("FattNonRicorsivo di ", n, ": ", ris2, " in ", finish-start, " s.")


# Es 5 -------------------------------------------------------
print("\n\nEs 5\n")

print(pi)
print(g)

densities = {"Al":[0.5,1,2],"Fe":[3,4,5],"Pb": [15,20,30]}
radii = [1,2,3]

#utilFuncs = [lambda r : 2 * pi * r , lambda r : pi * r**2 , lambda r : 4 * pi * r**3 / 3.0]
#utilFuncs = [lambda r : 2 * pi * r**i / i (if i == 3 lambda r : 4 * pi * r**i / i)  for i in range(1,4)]
utilFuncs = [lambda r : c * pi * r**p for c, p in zip([2.0, 1.0, 4.0/3.0],[1, 2, 3])]


r = radii[1]
riss = utilFuncs[0](r)
print(riss)

for elem in densities.keys():
    print("Elemento: ", elem)
    for r in radii:
        print("Raggio r = ", r)
        for d,i in zip(densities[elem], utilFuncs):
            print("Peso del corpo = ", d * i(r))
        #enddo
    #enddo
#enddo
