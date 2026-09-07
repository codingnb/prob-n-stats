import random
import time
import matplotlib.pyplot as plt

price = 100

prices = []

movements = 0

playing = True
while playing:
    new_price = random.uniform(-5,5)
    print(round(price, 2))
    movements += 1
    if price >= 120:
        new_price = random.uniform(-10, 1)
        movements += 1
    elif price <= 80:
        new_price = random.uniform(-1, 10)
        movements += 1
    else:
        new_price = random.uniform(-5, 5)
    if movements >= 100:
        playing = False
    price = price + new_price
    prices.append(price)

print("Simulation complete")
print("Highest Price: ", round(max(prices), 2))
print("Lowest Price: ", round(min(prices), 2))
print("Starting Price: ", "100")
print("Ending Price: ", round(price, 2))
price_return = (price - 100) / 100 * 100
print("Price Return: ", round(price_return, 2))
plt.plot(prices)
plt.show()