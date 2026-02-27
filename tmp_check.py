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
    
    time.sleep(2)
