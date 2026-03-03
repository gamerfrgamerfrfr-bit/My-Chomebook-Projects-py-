import time
import shutil
import os
import subprocess

# --- 1. Settings & Colors ---
BLUE, RED, GREEN, YELLOW = "\033[94m", "\033[91m", "\033[92m", "\033[93m"
MAGENTA, CYAN, WHITE, BOLD, END = "\033[95m", "\033[96m", "\033[97m", "\033[1m", "\033[0m"

# --- 2. Data Functions ---

def get_cpu_model():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if "model name" in line or "Processor" in line:
                    return line.split(':')[1].strip()
    except: return "Unknown CPU"

def get_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            seconds = float(f.readline().split()[0])
        return f"{int(seconds // 3600)}h {int((seconds % 3600) // 60)}m"
    except: return "N/A"

def get_temp():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            return int(f.read().strip()) // 1000
    except: return 0

def get_latency():
    try:
        output = subprocess.check_output(["ping", "-c", "1", "-W", "1", "8.8.8.8"], stderr=subprocess.STDOUT, universal_newlines=True)
        if "time=" in output:
            return float(output.split("time=")[1].split(" ")[0])
    except: return None

def get_battery():
    # Looks for any battery folder (BAT0, BAT1, etc.)
    base_path = "/sys/class/power_supply/"
    for folder in os.listdir(base_path):
        if folder.startswith("BAT") or "battery" in folder.lower():
            try:
                with open(os.path.join(base_path, folder, 'capacity'), 'r') as f:
                    percent = f.read().strip()
                with open(os.path.join(base_path, folder, 'status'), 'r') as f:
                    status = f.read().strip()
                icon = "⚡" if status == "Charging" else "🔋"
                return f"{percent}% {icon}"
            except: continue
    return "N/A"

def draw_bar(current, total, width=20):
    if total <= 0: return "[ ]"
    percent = min(current / total, 1.0) # <--- FIX: Limits bar to 100% max
    color = RED if percent > 0.8 else YELLOW if percent > 0.5 else GREEN
    filled = int(width * percent)
    bar = f"{color}" + ("#" * filled) + f"{END}" + ("-" * (width - filled))
    return f"[{bar}] {color}{int(percent*100)}%{END}"

# --- 3. Main Loop ---

try:
    while True:
        # Gather Data
        temp_num = get_temp()
        ms = get_latency()
        bat = get_battery()
        
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        
        # RAM & Swap
        total_kb = int(lines[0].split()[1])
        used_kb = total_kb - int(lines[1].split()[1])
        s_total, s_free = 0, 0
        for line in lines:
            if "SwapTotal" in line: s_total = int(line.split()[1])
            if "SwapFree" in line: s_free = int(line.split()[1])
        s_used = s_total - s_free

        # Disk Math (Improved)
        d_used, d_total = shutil.disk_usage("/")[:2]

        # Network Logic
        if ms is None:
            net_status = f"{RED}OFFLINE ❌{END}"
        else:
            n_clr = GREEN if ms < 60 else YELLOW if ms < 150 else RED
            net_status = f"{n_clr}{ms}ms{END}"

        # UI Rendering
        print("\033[H\033[J") 
        print(f"{YELLOW}{BOLD}--- CHROMEBOOK ULTIMATE DASHBOARD ---{END}")
        print(f"{GREEN} CPU:    {get_cpu_model()}{END}")
        print(f"{CYAN} UPTIME: {get_uptime()}{END}")
        print(f"{BLUE} NET:    {net_status}{END}")
        print(f"{YELLOW} BATT:   {bat}{END}")
        print(f"{MAGENTA} TEMP:   {END}{WHITE}{temp_num}°C{END}")
        print(f" RAM:    {draw_bar(used_kb, total_kb)} {WHITE}({used_kb//1024}MB){END}")
        print(f" STRESS: {draw_bar(s_used, s_total)} {WHITE}(Swap){END}")
        print(f" DISK:   {draw_bar(d_used, d_total)} {WHITE}({d_used//(1024**3)}GB){END}")
        print(f"{YELLOW}---------------------------------------{END}")
        print(f"{BOLD}{RED}Press Ctrl+C to exit{END}")
        
        time.sleep(2)

except KeyboardInterrupt:
    print(f"\n{GREEN}Dashboard closed. Great session, Bob!{END}")
