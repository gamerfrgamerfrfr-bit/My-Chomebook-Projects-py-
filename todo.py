import os

TODO_FILE = "my_tasks.txt"

# ANSI Colors
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"

def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as f:
        return [line.strip() for line in f.readlines()]

def save_tasks(tasks):
    with open(TODO_FILE, "w") as f:
        for task in tasks:
            f.write(task + "\n")

def main():
    tasks = load_tasks()
    
    while True:
        print(f"\n{GREEN}--- SMART TO-DO LIST ---{RESET}")
        for i, item in enumerate(tasks, 1):
            # Split the task text from the priority number
            parts = item.split("|")
            text = parts[0]
            priority = parts[1] if len(parts) > 1 else "3"

            # Choose color based on priority
            color = GREEN
            if priority == "1": color = RED
            elif priority == "2": color = YELLOW
            
            print(f"{i}. {color}{text}{RESET}")
        
        print(f"\nOptions: [{YELLOW}a{RESET}] Add, [{RED}d{RESET}] Delete, [{YELLOW}q{RESET}] Quit")
        choice = input("Choice: ").lower()

        if choice == 'a':
            text = input("Task description: ")
            prio = input("Priority (1=High, 2=Med, 3=Low): ")
            tasks.append(f"{text}|{prio}")
            save_tasks(tasks)
        elif choice == 'd':
            num = int(input("Number to delete: "))
            if 0 < num <= len(tasks):
                tasks.pop(num - 1)
                save_tasks(tasks)
        elif choice == 'q':
            break

if __name__ == "__main__":
    main()
