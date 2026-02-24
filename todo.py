import os

# The name of the file where we will store our data
TODO_FILE = "my_tasks.txt"

def load_tasks():
    """Reads tasks from the file if it exists."""
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as f:
        # strip() removes the extra newline character from each line
        return [line.strip() for line in f.readlines()]

def save_tasks(tasks):
    """Writes the current list of tasks to the file."""
    with open(TODO_FILE, "w") as f:
        for task in tasks:
            f.write(task + "\n")

def main():
    tasks = load_tasks()
    
    while True:
        print("\n--- CHROMEBOOK TO-DO LIST ---")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")
        
        print("\nOptions: [a] Add, [d] Delete, [q] Quit")
        choice = input("Choose an option: ").lower()

        if choice == 'a':
            new_task = input("Enter the task: ")
            tasks.append(new_task)
            save_tasks(tasks)
        elif choice == 'd':
            num = int(input("Enter the task number to delete: "))
            if 0 < num <= len(tasks):
                tasks.pop(num - 1)
                save_tasks(tasks)
        elif choice == 'q':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
