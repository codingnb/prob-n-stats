import random

One = 0
Two = 0
Three = 0
Four = 0
Five = 0
Six = 0

amount = int(input("How many times would you like to roll the dice?"))

for _ in range(amount):
    roll = random.choice([1,2,3,4,5,6])
    
    if roll == 1:
        One += 1
    if roll == 2:
        Two += 1
    if roll == 3:
        Three += 1
    if roll == 4:
        Four += 1
    if roll == 5:
        Five += 1
    if roll == 6:
        Six += 1

print("Ones", One)
print("Twos", Two)
print("Threes", Three)
print("Fours", Four)
print("Fives", Five)
print("Sixes", Six)
print("Number percentage:")
print("Ones:", One / amount * 100)
print("Twos:", Two / amount * 100)
print("Threes:", Three / amount * 100)
print("Fours:", Four / amount * 100)
print("Fives:", Five / amount * 100)
print("Sixes:", Six / amount * 100)
