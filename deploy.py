import sys
import os
import time

def deploy(action="deploy"):
    env_file = "current_env.txt"
    
    # Read current state (default to none)
    current = "none"
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            current = f.read().strip()
            
    # Handle the Rollback Requirement
    if action == "rollback":
        if current == "green":
            print("[*] Rolling back to Blue environment...")
            new_env, port = "blue", 8001
        elif current == "blue":
            print("[*] Rolling back to Green environment...")
            new_env, port = "green", 8002
        else:
            print("[-] No active environment to roll back from.")
            return
            
    # Handle Standard Deployment
    else: 
        if current == "blue":
            print("[*] Deploying update to Green environment...")
            new_env, port = "green", 8002
        else:
            print("[*] Deploying update to Blue environment...")
            new_env, port = "blue", 8001

    # Start the app on the target port
    print(f"[*] Starting application on port {port}...")
    if sys.platform == "win32":
        # Windows command to run Uvicorn in the background
        os.system(f"start /B uvicorn main:app --port {port}")
    else:
        # Mac/Linux command
        os.system(f"uvicorn main:app --port {port} &")
        
    time.sleep(2) # Give the server a second to boot
    
    # Save the new state
    with open(env_file, "w") as f:
        f.write(new_env)
        
    print(f"[+] Success! Traffic is now simulated on {new_env.upper()} (http://127.0.0.1:{port})")

if __name__ == "__main__":
    action = "deploy"
    # Check if we passed the --rollback flag
    if len(sys.argv) > 1 and sys.argv[1] == "--rollback":
        action = "rollback"
    deploy(action)