s="Write a program that prints the numbers from 1 to 100. \
But for multiples of three print Mickey instead of the number and for the multiples of five print Mouse. \
For numbers which are multiples of both three and five print MickeyMouse"

lows=s.lower()
ldict = {None : None}
del ldict[None]
for c in lows:
    if c in ldict:
        ldict[c]=ldict[c]+1
    else:
        ldict[c]=1
print(ldict)

