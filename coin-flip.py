import random

flipping = True

heads = 0
tails = 0

amount = 0

if flipping is True:
    amount = int(input("How many times would you like to flip the coin?"))
    for _ in range(amount):
        flip = random.choice(["heads", "tails"])
    
        if flip == "heads":
            heads += 1
        else:
            tails += 1
    
    print("Heads:", heads)
    print("Tails:", tails)
    print("Heads percentage:", heads / amount * 100)