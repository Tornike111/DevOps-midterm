import os
import subprocess
import sys

def run_command(command, description):
    print(f"[*] {description}...")
    try:
        subprocess.run(command, check=True, shell=True)
        print("[+] Success!\n")
    except subprocess.CalledProcessError as e:
        print(f"[-] Failed: {e}")
        sys.exit(1)

def setup_environment():
    print("=== Starting Infrastructure Setup ===\n")

    # 1. Create necessary deployment directories
    dirs = ["logs", "production_env"]
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"[+] Created directory: {d}")
        else:
            print(f"[*] Directory already exists: {d}")
    print()

    # 2. Set up an isolated virtual environment
    venv_dir = "venv"
    if not os.path.exists(venv_dir):
        run_command(f"{sys.executable} -m venv {venv_dir}", "Creating virtual environment")
    else:
        print("[*] Virtual environment already exists.\n")

    # 3. Install dependencies
    if os.name == 'nt': # Windows
        pip_path = os.path.join(venv_dir, "Scripts", "pip")
    else: # Mac/Linux
        pip_path = os.path.join(venv_dir, "bin", "pip")

    dependencies = "fastapi uvicorn pytest httpx pydantic"
    run_command(f"{pip_path} install {dependencies}", "Installing required packages")

    print("=== Infrastructure Setup Complete! ===")

if __name__ == "__main__":
    setup_environment()