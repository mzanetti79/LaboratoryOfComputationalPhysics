mylist = [None]
for i in range(1,101):
    if i % 15 == 0:
        #print("MickeyMouse")
        mylist.append("MickeyMouse")
    elif i % 3 == 0:
        #print("Mickey")
        mylist.append("Mickey")

    else:
        #print(i)
        mylist.append(i)

mylist = ["Donald" if x=="Mickey" else x for x in mylist]
mylist = ["DonaldDuck" if x=="MickeyMouse" else x for x in mylist]

print(mylist)
