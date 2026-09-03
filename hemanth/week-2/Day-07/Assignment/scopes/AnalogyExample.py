hero = "Mahesh Babu"

def Bussiness_Man():
    hero = "Gautam"
    print(hero) 

def change_global():
    global hero
    hero = "Krishna"
    print(hero)

#printing local hero
Bussiness_Man()#Gautam will be printed

#printing global hero
print(hero)#Mahesh 

#printing changed global hero
change_global()#Krsihna 

#trying to print global scope variable which was changed
print(hero) #krishna