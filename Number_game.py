import random
# ... Colors to use! ... #
RED = "\033[91m"
BLUE = "\033[94m"
END = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BOLD = "\033[1m"
END = "\033[0m"

# --- Difficulty ---
print(f"{CYAN}--- CHOOSE YOUR DESTINY ---{END}")
print(f"1. {GREEN}Easy (1-10){END}")
print(f"2. {RED}Hard (1-100){END}")

choice = input(f"{BOLD}Select mode (1 or 2): {END}")

# ---  Sets lives ---
if choice == "2":
    limit = 100
    lives = 5  # Hard mode gets 5 tries
    mode_name = f"{RED}HARD{END}"
else:
    limit = 10
    lives = 3  # Easy mode gets 3 tries
    mode_name = f"{GREEN}EASY{END}"

secret_number = random.randint(1, limit)
print(f"\n{BOLD}Mode set to {mode_name}. You have {lives} lives!{END}")

# --- 2. The Game Loop ---
while lives > 0:
        # --- Pick the Life Color ---
        if lives >= 3:
            life_color = GREEN
        elif lives == 2:
            life_color = YELLOW
        else:
            life_color = RED  

        guess = int(input(f"\n{WHITE}Guess (1-{limit}): {END}"))

        if guess == secret_number:
            print(f"{GREEN}{BOLD}✨ CORRECT! YOU WIN! ✨{END}")
            break
        
        else:
            lives -= 1
            if lives > 0:
                print(f"{RED}Incorrect!{END}")
                
                # --- The hint  ---
                if guess > secret_number:
                    print(f"{CYAN}Hint: Try a LOWER number. ↓{END}")
                else:
                    print(f"{MAGENTA}Hint: Try a HIGHER number. ↑{END}")
                
                # --- Show remaining lives And the color ---
                print(f"Lives remaining: {life_color}{lives}{END}")
            else:
                print(f"{RED}{BOLD}GAME OVER!{END} The number was {YELLOW}{secret_number}{END}.")
