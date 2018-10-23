#
# Esercitazione 04
# LaboratoryOfComputationalPhysics
#
#

# Same old story over and over again

import numpy as np
import time
import math


# Es 1 -------------------------
print("\n\nEs 1\n")

# RICORDO: se converto da intero a binario o esadecimale,
# quello che si ottiene e` una stringa!
# quindi il returntype della funzione che ritorna la
# rappresentazione binaria del numero e` string

def convertToBinary(n):
    strRet = bin(n)
    return strRet
#enddef

def convertBinary(n):
    tmp = n
    listBin = []
    while tmp != 0:
        if tmp%2 == 0:
            listBin.append('0')
            tmp = tmp // 2
        elif tmp%2 != 0:
            listBin.append('1')
            tmp = tmp // 2
        #endif
    #enddo
    listBin.reverse()
    strBin = ''.join(listBin)
    return strBin
#enddef
 

n = 1945
print("Intero n = ", n)
print("Rappresentazione di n in binario = ", convertToBinary(n))
#print(n)
print("Rappresentazione di n in binario = ", convertBinary(n))

# altrimenti
print("Rappresentazione in binario {0:08b}".format(n))
print(n) # sinceriamoci che la funzione non abbia alterato il valore di n


# Es 2 ------------------------------
print("\n\nEs 2\n")

strInt = '00110111001000100010111000110011'
strInt = '00000011111000000000000000000000'
print(len(strInt))

print(type(strInt[0:22+1]))

f = int( strInt[0:22+1] , 2 )
e = int( strInt[23:30+1] , 2 )
s = int( strInt[31] , 2)

xFloat = (-1)**2 * (1 + 0.1 * f) * 2**(e - 127)
print(xFloat)


# Es 3 ------------------------------------------
print("\n\nEs 3\n")
