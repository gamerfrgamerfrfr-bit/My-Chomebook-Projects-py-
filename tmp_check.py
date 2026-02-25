import time

# Colors
BLUE = "\033[94m"
RED = "\033[91m"
END = "\033[0m"
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
        # Convert from millidegrees to degrees
        return f"{int(temp_raw) // 1000}°C"
    except:
        return "N/A"


while True:
    cpu = get_cpu_model()
    up = get_uptime()
    temp = get_temp()  # New tool!
    
    # ...  RAM calculation code ...

    with open('/proc/meminfo', 'r') as f:
        lines = f.readlines()
    
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
