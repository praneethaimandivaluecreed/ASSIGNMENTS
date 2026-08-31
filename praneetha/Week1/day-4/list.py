#creating a list
a = ['a',"pranee",34]
print(a)
print(type(a))

#using constructor list()
b = list("pranee")
c = list([23,"abc"])
s1,s2 = c
print(s1)
print(s2)
print(b)
print(c)

#list with repeated elements
d = ["praneetha"] * 6
print(d)

#accessing the lists
print(a[1])
print(a[-1])


#adding elements
#1.append() - adds at the end
d.append("Imandi")
print(d)

#2.insert - at a specific pos
d.insert(2,"niha")
print(d)

#3.extend() - adds multiple elements at end
d.extend([1,2])
print(d)


#updating the list
d[2] = "niharika"
print(d)



#removing elements from a list
#1.remove() - removes first occurence of elements in the list & error if not present
d.remove("praneetha")
print(d)

#2.pop() - removes elements at specific index & last if not specified
d.pop()
print(d)

#3.del - deletes elements at speciifc index
del d[2]
print(d)

#4.clear() - removes all elements
d.clear()
print(d)

q = ("pranee")
print(type(q))