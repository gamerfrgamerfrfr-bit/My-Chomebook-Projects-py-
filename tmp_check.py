

import time
import shutil



# Colors
BLUE = "\033[94m"
RED = "\033[91m"
END = "\033[0m"


def get_cpu_model():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if "model name" in line or "Processor" in line:
                    return line.split(':')[1].strip()
    except Exception:
        return "Unknown CPU"
    return "Unknown CPU"

def get_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            seconds = float(f.readline().split()[0])
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"
    except Exception:
        return "N/A"


#
def get_cpu_model():
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if "model name" in line or "Processor" in line:
                return line.split(':')[1].strip()
    return "Unknown CPU"
#####################################################################
def get_uptime():
    with open('/proc/uptime', 'r') as f:
        seconds = float(f.readline().split()[0])
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{hours}h {minutes}m"
#####################################################################
def get_ram_usage():
    with open('/proc/meminfo', 'r') as f:
        lines = f.readlines()
    
    # Total memory is usually the 1st line, Free is the 2nd or 3rd
    total_kb = int(lines[0].split()[1])
    free_kb = int(lines[1].split()[1])
    
    # Calculate used RAM in Megabytes
    used_mb = (total_kb - free_kb) // 1024
    total_mb = total_kb // 1024
    
    return f"{used_mb}MB / {total_mb}MB"

############################################################################
def draw_bar(current, total, width=20):
           # Calculate what percentage is full
            percent = current / total
            # Calculate how many hashtags to show
            filled_length = int(width * percent)
            # Create the bar string
            bar = "#" * filled_length + "-" * (width - filled_length)
            return f"[{bar}] {int(percent * 100)}%"
###################################################################################

def get_temp():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp_raw = f.read().strip()

        return int(temp_raw) // 1000 
    except Exception:
        return 0

def get_disk_usage():
    try:
        # Checks the root (/) partition where your 14GB is
        total, used, free = shutil.disk_usage("/")
        return used, total
    except Exception:
        return 0, 0

def draw_bar(current, total, width=20):
    if total <= 0: return "[--------------------] 0%"
    percent = min(1.0, current / total)
    filled_length = int(width * percent)
    bar = "#" * filled_length + "-" * (width - filled_length)
    return f"[{bar}] {int(percent * 100)}%"

# --- MAIN LOOP ---
while True:
    # 1. Gather Data
    cpu = get_cpu_model()
    up = get_uptime()
    temp_num = get_temp()
    
    # 2. RAM Calculation
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        total_kb = int(lines[0].split()[1])
        avail_kb = int(lines[2].split()[1]) 
        used_kb = total_kb - avail_kb
        ram_bar = draw_bar(used_kb, total_kb)
        used_ram_mb = used_kb // 1024
        total_ram_mb = total_kb // 1024
    except Exception:
        ram_bar = "[Error]"
        used_ram_mb, total_ram_mb = 0, 0

    # 3. Storage Calculation
    d_used, d_total = get_disk_usage()
    storage_bar = draw_bar(d_used, d_total)
    # Convert bytes to GB for the text display
    used_gb = d_used / (1024**3)
    total_gb = d_total / (1024**3)

    # 4. Temperature Status Color
    status = f"{RED}HOT! 🔥{END}" if temp_num > 65 else f"{BLUE}COOL ❄️{END}"

    # 5. Display Output
    print("\033[H\033[J", end="") # Clears screen
    print("--- CHROMEBOOK DASHBOARD ---")
    print(f"CPU:     {cpu}")
    print(f"UPTIME:  {up}")
    print(f"TEMP:    {temp_num}°C ({status})")
    print(f"RAM:     {ram_bar} ({used_ram_mb}MB / {total_ram_mb}MB)")
    print(f"STORAGE: {storage_bar} ({used_gb:.1f}GB / {total_gb:.1f}GB)")
    print("----------------------------")
    print("Press Ctrl+C to exit")

        # Convert from millidegrees to degrees
        return f"{int(temp_raw) // 1000}°C"

    
    # Colors

# Colors

BLUE = "\033[94m"
RED = "\033[91m"
END = "\033[0m"

def get_cpu_model():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if "model name" in line or "Processor" in line:
                    return line.split(':')[1].strip()


    except:
            return "Unknown CPU"

    except Exception:
        return "Unknown CPU"

    return "Unknown CPU"

def get_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            seconds = float(f.readline().split()[0])
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"
    except Exception:
        return "N/A"

def get_temp():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp_raw = f.read().strip()
        return int(temp_raw) // 1000 
    except Exception:
        return 0

def get_disk_usage():
    try:
        # Checks the root (/) partition where your 14GB is
        total, used, free = shutil.disk_usage("/")
        return used, total
    except Exception:
        return 0, 0

def draw_bar(current, total, width=20):
    if total <= 0: return "[--------------------] 0%"
    percent = min(1.0, current / total)
    filled_length = int(width * percent)
    bar = "#" * filled_length + "-" * (width - filled_length)
    return f"[{bar}] {int(percent * 100)}%"

# --- MAIN LOOP ---
while True:
    # 1. Gather Data
    cpu = get_cpu_model()
    up = get_uptime()
    temp_num = get_temp()
    
    # 2. RAM Calculation
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        total_kb = int(lines[0].split()[1])
        avail_kb = int(lines[2].split()[1]) 
        used_kb = total_kb - avail_kb
        ram_bar = draw_bar(used_kb, total_kb)
        used_ram_mb = used_kb // 1024
        total_ram_mb = total_kb // 1024
    except Exception:
        ram_bar = "[Error]"
        used_ram_mb, total_ram_mb = 0, 0

    # 3. Storage Calculation
    d_used, d_total = get_disk_usage()
    storage_bar = draw_bar(d_used, d_total)
    # Convert bytes to GB for the text display
    used_gb = d_used / (1024**3)
    total_gb = d_total / (1024**3)

    # 4. Temperature Status Color
    status = f"{RED}HOT! 🔥{END}" if temp_num > 65 else f"{BLUE}COOL ❄️{END}"

    # 5. Display Output
    print("\033[H\033[J", end="") # Clears screen
    print("--- CHROMEBOOK DASHBOARD ---")
    print(f"CPU:     {cpu}")
    print(f"UPTIME:  {up}")
    print(f"TEMP:    {temp_num}°C ({status})")
    print(f"RAM:     {ram_bar} ({used_ram_mb}MB / {total_ram_mb}MB)")
    print(f"STORAGE: {storage_bar} ({used_gb:.1f}GB / {total_gb:.1f}GB)")
    print("----------------------------")
    print("Press Ctrl+C to exit")
    

        # 3. Temperature Logic
        if temp_num > 65: # ARMv7 chips get hot around 65-70C
            status = f"{RED}HOT! 🔥{END}"
        else:
            status = f"{BLUE}COOL ❄️{END}"
    

    total_mb = int(lines[0].split()[1])
    free_mb = int(lines[1].split()[1])
    used_mb = total_mb - free_mb
    
    # 2. Generate the bar using MB (math stays accurate)
    ram_bar = draw_bar(used_mb, total_mb)
    
    # 3. Convert to MB just for the labels
    used_mb = used_mb // 1024
    total_mb = total_mb // 1024

    print("\033[H\033[J") 
    print("--- CHROMEBOOK DASHBOARD ---")
    print(f"CPU:    {cpu}")
    print(f"TEMP:   {temp}") 
    print(f"RAM:    {draw_bar}")
    print(f"Uptime: {up}")
   

    temp_str = get_temp() 
    temp_num = int(temp_str[:-2])
    if temp_num > 70:
        status = f"{RED}HOT! 🔥{END}"
    else:
        status = f"{BLUE}COOL ❄️{END}"

    print(f"TEMP:   {temp_str} ({status})")
    print("----------------------------")

    
    time.sleep(2)

        # 4. Printing (Clear screen and show dashboard)
        print("\033[H\033[J", end="") # Clears terminal
        print("--- CHROMEBOOK DASHBOARD ---")
        print(f"CPU:    {cpu}")
        print(f"UPTIME: {up}")
        print(f"TEMP:   {temp_num}°C ({status})")
        print(f"RAM:    {ram_bar_visual} ({used_mb}MB / {total_mb}MB)")
        print("----------------------------")
        print("Press Ctrl+C to exit")
        
        time.sleep(2)


    time.sleep(2)

