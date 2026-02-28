import time
import shutil
import os

# --- 1. Settings & Colors ---
BLUE = "\033[R94m"
RED = "\033[91m"
END = "\033[0m"

# --- 2. Data Functions ---

def get_cpu_model():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if "model name" in line or "Processor" in line:
                    return line.split(':')[1].strip()
    except:
        return "Unknown CPU"

def get_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            seconds = float(f.readline().split()[0])
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"
    except:
        return "N/A"

def get_temp():
    try:
        
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp_raw = f.read().strip()
        return int(temp_raw) // 1000
    except:
        return 0

def get_disk_usage():
    try:
        total, used, free = shutil.disk_usage("/")
        return used, total
    except:
        return 0, 0

def draw_bar(current, total, width=20):
    if total <= 0: return "[ ]"
    percent = current / total
    filled = int(width * percent)
    bar = "#" * filled + "-" * (width - filled)
    return f"[{bar}] {int(percent*100)}%"

# --- 3. Main Loop ---

while True:
    
    cpu = get_cpu_model()
    uptime = get_uptime()
    temp_num = get_temp()
    
    
    with open('/proc/meminfo', 'r') as f:
        lines = f.readlines()
    total_kb = int(lines[0].split()[1])
    free_kb = int(lines[1].split()[1])
    used_kb = total_kb - free_kb
    
    
    d_used, d_total = get_disk_usage()
    
    
    if temp_num > 70:
        status = f"{RED}HOT! 🔥{END}"
    elif temp_num > 50:
        status = "WARM ☀️"
    else:
        status = f"{BLUE}COOL ❄️{END}"

    
    print("\033[H\033[J") 
    print("--- CHROMEBOOK DASHBOARD ---")
    print(f"CPU:    {cpu}")
    print(f"UPTIME: {uptime}")
    print(f"TEMP:   {temp_num}°C ({status})")
    print(f"RAM:    {draw_bar(used_kb, total_kb)} ({used_kb//1024}MB / {total_kb//1024}MB)")
    print(f"DISK:   {draw_bar(d_used, d_total)} ({d_used//(1024**3)}GB / {d_total//(1024**3)}GB)")
    print("----------------------------")
    print("Press Ctrl+C to exit")
    
    time.sleep(2)
