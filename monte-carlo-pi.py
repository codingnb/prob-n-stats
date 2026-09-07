import random

points = int(input("How many points would you like to generate? "))

circle = 0
for _ in range(points):
    y = random.uniform(-1, 1)
    x = random.uniform(-1, 1)

    if x ** 2 + y ** 2 <= 1:
        circle += 1
        
piest = 4 * circle / points
theoretical = 3.141592653589793
difference = abs(piest - theoretical)
print(piest)
print("Theoretical pi: ", 3.14159)
print("Experimental Pi: ", piest)
print("Difference: ", round(difference, 4))