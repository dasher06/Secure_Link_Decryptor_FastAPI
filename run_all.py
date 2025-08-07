import subprocess
import threading
import time
import os

def start_uvicorn():
    subprocess.run([
        "uvicorn", "decrypt_api:app", "--port", "8181"
    ])

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    server_thread = threading.Thread(target=start_uvicorn)
    server_thread.start()

    # Wait briefly to ensure FastAPI is ready
    time.sleep(2)

    # Run Encrypted_Link.py in same terminal process to support input/output
    os.system("python Encrypted_Link.py")
