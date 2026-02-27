import time
    
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
    return "Unknown CPU"
    
def get_uptime():
        with open('/proc/uptime', 'r') as f:
            seconds = float(f.readline().split()[0])
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"
    
def get_temp():
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp_raw = f.read().strip()
            return int(temp_raw) // 1000  # Return as an integer for math
        except:
            return 0
    
def draw_bar(current, total, width=20):
        if total == 0: return "[--------------------] 0%"
        percent = current / total
        filled_length = int(width * percent)
        # Ensure filled_length doesn't exceed width due to rounding
        filled_length = min(width, filled_length)
        bar = "#" * filled_length + "-" * (width - filled_length)
        return f"[{bar}] {int(percent * 100)}%"
    
    # --- MAIN LOOP ---
while True:
        # 1. Get Data
        cpu = get_cpu_model()
        up = get_uptime()
        temp_num = get_temp()
        
        # 2. RAM Calculation
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        
        # MemTotal is line 0, MemAvailable is usually line 2 (more accurate than MemFree)
        total_kb = int(lines[0].split()[1])
        available_kb = int(lines[2].split()[1]) 
        used_kb = total_kb - available_kb
        
        # Generate the bar using the raw KB for precision
        ram_bar_visual = draw_bar(used_kb, total_kb)
        
        # Convert to MB for the text label
        used_mb = used_kb // 1024
        total_mb = total_kb // 1024
    
        # 3. Temperature Logic
        if temp_num > 65: # ARMv7 chips get hot around 65-70C
            status = f"{RED}HOT! 🔥{END}"
        else:
            status = f"{BLUE}COOL ❄️{END}"
    
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
