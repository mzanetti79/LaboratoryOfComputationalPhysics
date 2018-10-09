# 
# Esercitazione 1
# LaboratoryOfComputationalPhysics
# 
# 

print("\n\nEs1\n1.a)\n\n")

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

print("\n\n1.b)\n")

for i in range(len(listToAdd)):
	if listToAdd[i] == "Misha":
		listToAdd[i] = "Donald"
	if listToAdd[i] == "MishaMouse":
		listToAdd[i] = "DonaldDuck"
#enddo

print(listToAdd)