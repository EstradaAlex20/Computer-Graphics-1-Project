import math

def points_on_circle(distance,amountOfPoints):
    angle = 360/amountOfPoints
    #print(angle)
    returnList = []
    startingAngle = 0
    for i in range(amountOfPoints):
        #print(startingAngle)
        x = distance * math.cos(math.radians(startingAngle))
        y = distance * math.sin(math.radians(startingAngle))
        startingAngle += angle
        returnList.append(x)
        returnList.append(y)
    return returnList

def indicies_list_gen(amountOfPoints):
    retList = []
    for i in range(amountOfPoints):
        retList.append(0)
        retList.append(i+2)
        retList.append(i+1)
    return retList


list1 = points_on_circle(10,50)
it = iter(list1)
for x in it:
    print("(" , x ,",", next(it) , ")")

print(indicies_list_gen(50))

[0.00,0.00,0.35,0.40,0.00,1.00,1.00,0.20,0.50,-0.25,-0.35,0.40,0.60,-0.95,-0.60,-0.95,0.00,-0.65,-1.00,0.20,-0.50,-0.25]
[0,1,2,3,0,1,3,4,0,0,5,2,0,4,6,7,8,0,0,8,6,0,9,5,0,9,10,0,10,7,0,9,10]