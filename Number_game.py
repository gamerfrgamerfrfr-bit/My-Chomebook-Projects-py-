import random

secret_number = random.randint(1,10)
guess = int(input("guess a number between 1 and 10:"))

if guess == secret_number:
    print("You got the number!")
else:
    print(f"Nope! It was {secret_number}")
