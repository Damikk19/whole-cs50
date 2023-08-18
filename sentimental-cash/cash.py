import cs50

while True:
    dollar = cs50.get_float("Enter your Change: ")
    if dollar > 0:
        break

cents = round(dollar * 100)
coins = 0

while cents >= 25:  # looking for 25 cents
    cents = cents - 25
    coins += 1

while cents >= 10:  # looking for 10 cents
    cents = cents - 10
    coins += 1

while cents >= 5:  # looking for 5 cents
    cents = cents - 5
    coins += 1

while cents >= 1:  # looking for 1 cents
    cents = cents - 1
    coins += 1

print(f"{coins}")