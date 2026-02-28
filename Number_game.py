import random
# ... Colors to use! ... #
RED = "\033[91m"
BLUE = "\033[R94m"
END = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BOLD = "\033[1m"
END = "\033[0m"

# ... Choose's the number ... #
secret_number = random.randint(1,10)

guess = int(input(f"{BOLD}{WHITE} Guess a number between 1 and 10:{END} "))

if guess == secret_number:
    print(f"{GREEN} You got the number!{END} ")
else:
    print(f"{RED} Nope!{END}{YELLOW} It was {secret_number}!{END}")
