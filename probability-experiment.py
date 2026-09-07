import random

flipping = True

heads = 0
tails = 0

amount = 0

while flipping:
    amount = int(input("How many times would you like to flip the coin? "))
    for _ in range(amount):
        flip = random.choice(["heads", "tails"])
        
        if flip == "heads":
            heads += 1
        else:
            tails += 1
    
    print("Heads:", heads)
    print("Tails:", tails)
    theoretical = 50
    experimental = round(heads / amount * 100, 1)
    difference = round(abs(theoretical - experimental), 1)
    print("Experimental probability of heads: ", round(heads / amount * 100), "%")
    print("Theoretical probability of heads: 50 %")
    print("Difference: ", difference, "%")
    heads = 0
    tails = 0
    amount = 0
    