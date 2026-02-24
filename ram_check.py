import time

def get_ram_usage():
    # Opening the system file that tracks memory
    with open('/proc/meminfo', 'r') as f:
        lines = f.readlines()
        
    # Extracting Total and Free memory (in kB)
    total_kb = int(lines[0].split()[1])
    free_kb = int(lines[1].split()[1])
    
    # Converting kB to GiB for easier reading
    total_gib = total_kb / (1024 * 1024)
    used_gib = (total_kb - free_kb) / (1024 * 1024)
    
    return total_gib, used_gib

print("--- Live RAM Monitor (Press Ctrl+C to stop) ---")

try:
    while True:
        total, used = get_ram_usage()
        # The :.2f makes it show only 2 decimal places
        print(f"RAM Used: {used:.2f} GiB / {total:.2f} GiB", end="\r")
        time.sleep(1) # Wait 1 second before checking again
except KeyboardInterrupt:
    print("\nStopped monitoring.")
