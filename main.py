# 
# Esercitazione 1
# LaboratoryOfComputationalPhysics
# 
# 

import time

# Es 1.a ---------------
print("\n\nEs1\n\n1.a)\n")

listToAdd = []

for i in range(1,100):
	if i % 3 == 0:
		print("Misha", i)
		listToAdd.append("Misha")
	if i % 3 == 0 and i % 5 == 0:
		print("MishaMouse", i)
		listToAdd.append("MishaMouse")
#enddo

print(listToAdd)

# Es 1.b ---------------
print("\n\n1.b)\n")

for i in range(len(listToAdd)):
	if listToAdd[i] == "Misha":
		listToAdd[i] = "Donald"
	if listToAdd[i] == "MishaMouse":
		listToAdd[i] = "DonaldDuck"
#enddo

print(listToAdd)

# Es 2 ------------------
print("\n\nEs2\n")

def Swap(x,y):

	toSwap = [x,y]
	toSwap.reverse()
	
	return toSwap[0], toSwap[1]
#enddef

cyka = 3
blyat = 6

print("cyka blyat = ", cyka, blyat)
cyka, blyat = Swap(cyka,blyat)
print("cyka blyat = ", cyka, blyat)


# Es 3 ----------------
print("\n\nEs 3\n")

def dist(x1, x2):
	
	# dist = || (x1 - y1)^2 + (x2 - y2)^2 ||^0.5
	d = ( (x1[0] - x2[0])**2 + (x1[1] - x2[1])**2 )**(1/2)
	return d
#enddef

x1 = [3.0, 0.0]
x2 = [0.0, 4.0]

d = dist(x1,x2)

print("Distanza = ", d)


# Es 4 -----------
print("\n\nEs 4\n")

s = "Write a program that prints the numbers from 1 to 100. \
     But for multiples of three print Mickey instead of the number and for the multiples of five print Mouse. \
     For numbers which are multiples of both three and five print MickeyMouse"

print(s)
	 
s = s.lower()
lettere = [c for c in s]


dictCheck = { }
matches = [chrs for chrs in lettere if chrs == lettere[0]]
dictCheck.update({ lettere[0] : len(matches) })
for i in range(1,len(lettere)):
	if i not in dictCheck.keys():
		matches = [chrs for chrs in lettere if lettere[i] == chrs]
		dictCheck.update({ lettere[i] : len(matches) })
	#endif
#enddo	

for keys in dictCheck:
	print(keys , dictCheck[keys])
#enddo
	
'''
for c in lettere:
	matches = [chrs for chrs in lettere if c == chrs]
	print("La lettera ", c, "compare nella lista ", len(matches), " volte")
	
#enddo
'''


# Es 5 ----------
print("\n\nEs 5\n")

l = [36, 45, 58, 3, 74, 96, 64, 45, 31, 10, 24, 19, 33, 86, 99, 18, 63, 70, 85,
 85, 63, 47, 56, 42, 70, 84, 88, 55, 20, 54, 8, 56, 51, 79, 81, 57, 37, 91,
 1, 84, 84, 36, 66, 9, 89, 50, 42, 91, 50, 95, 90, 98, 39, 16, 82, 31, 92, 41,
 45, 30, 66, 70, 34, 85, 94, 5, 3, 36, 72, 91, 84, 34, 87, 75, 53, 51, 20, 89, 51, 20]
 
def CountUniques(listNumbers):
	
	listUniques = [ ]
	for nums in listNumbers:
		matches = [n for n in listNumbers if n == nums]
		if len(matches) == 1:
			listUniques.append(nums)
		#endif
	#enddo
	return listUniques
#enddef

unici = CountUniques(l)

print(unici)

print("I numeri unici sono: ", len(unici), " mentre la lista di numeri è di ", len(l))
	


# Es 6 -----------

print("\n\nEs 6\n")

def Square(n):
	ris = n**2
	return ris
#enddef

def Cube(n):
	ris = n**3
	return ris
#enddef

def SixthPower(m):
	#ris = Square(m)
	#ris = Cube(ris)
	ris = Square(Cube(m))
	return ris
#enddef

pizdec = 2
ris = SixthPower(pizdec)
print("La sesta potenza di", pizdec, " è ", ris)
 
# Es 7 -----------
print("\n\nEs 7\n\n7.a)\n")
 
listCubes = []
 
for i in range(10+1):
	listCubes.append(i**3)
#enddo
	
print(listCubes)
	
print("\n7.b)\n")
listCubes = [n**3 for n in range(0,10+1)]	

print(listCubes)


# Es 8 ------------
print("\n\nEs 8\n")

listTuples = []

start = time.time()

for i in range(1,100):
	for j in range(i,100):
		for k in range(j,100):
			ans = abs(k**2 - i**2 - j**2)
			if ans == 0:
				listTuples.append( (i,j,k) )
			#endif
		#enddo
	#enddo
#enddo
end = time.time()
print("Con for innestati: ", end - start, " s.")

print(listTuples)


# tuple2 = [ [ [ [i for i in range(1,100)] for j in range(i,100) ] for k in range(1,100) ] if k**2 - i**2 - j**2 == 0 ]
start = time.time()

listToTuple = [ (i, j, k) for i in range(1,100) for j in range(i,100) for k in range(j,100) if k**2 - i**2 - j**2 == 0 ]

end = time.time()
print("\nCon list comprehension: ", end - start, " s.")	

print(listToTuple)


# Es 9 --------

print("\n\nEs 9\n")

tupleToNorm = (0, 0, 1, 3, 4, 6, 7, 9, 10, 5, 3, 2, 1, 2, 0, 1, 0)
listNorm = [n/max(tupleToNorm) for n in tupleToNorm]
tupleNorm = tuple(listNorm)

print(tupleToNorm)
print(tupleNorm)












