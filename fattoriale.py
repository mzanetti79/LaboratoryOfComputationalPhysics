n = int(input("Inserisci un numero di cui vuoi calcolare il fattoriale: "))

fatt = 1

if n >= 0:
	while n>0:
		fatt = fatt*n
		n -= 1
else:
	print("Non si puo' calcolare il fattoriale di questo numero")

print(fatt)
