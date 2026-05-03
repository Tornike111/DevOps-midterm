import time
import requests
import os
from datetime import datetime

LOG_FILE = "logs/health_check.log"
ENV_FILE = "current_env.txt"

def check_health():
    print(f"[*] Starting health monitor. Logging to {LOG_FILE}. Press CTRL+C to stop.")
    
    # Ensure our log directory exists
    if not os.path.exists("logs"):
        os.makedirs("logs")

    while True:
        # Determine which port we should be checking
        port = 8001 # Default to blue
        if os.path.exists(ENV_FILE):
            with open(ENV_FILE, "r") as f:
                if f.read().strip() == "green":
                    port = 8002
        
        url = f"http://127.0.0.1:{port}/"
        
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                status = "UP"
            else:
                status = f"ERROR ({response.status_code})"
        except requests.exceptions.RequestException:
            status = "DOWN (Connection Refused)"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        env_name = 'BLUE' if port == 8001 else 'GREEN'
        log_entry = f"[{timestamp}] Environment: {env_name} | Port: {port} | Status: {status}\n"
        
        # Write to the file
        with open(LOG_FILE, "a") as f:
            f.write(log_entry)
        
        # Print to the console
        print(log_entry.strip())
        time.sleep(5)

if __name__ == "__main__":
    check_health()