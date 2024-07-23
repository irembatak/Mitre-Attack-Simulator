import tkinter as tk
import subprocess
import os
import sys
import socket
from datetime import datetime
from firebase_admin import credentials, db, initialize_app

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Firebase yapılandırması
config_path = resource_path('firebase_config.json')
cred = credentials.Certificate(config_path)
initialize_app(cred, {
    'databaseURL': 'https://cyber-32dd2-default-rtdb.firebaseio.com/'
})

def get_computer_name():
    return socket.gethostname()

def send_data_to_firebase(path, data):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    ref = db.reference(f"{path}/{timestamp}")
    ref.set(data)

def run_script(script_name):
    script_path = resource_path(script_name)
    try:
        result = subprocess.run(
            ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", script_path],
            capture_output=True,
            text=True
        )
        return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)

def run_t1649():
    computer_name = get_computer_name()
    output, error = run_script('t1649.ps1')
    if error:
        send_data_to_firebase('/attack_results/T1649', {"output": error, "computer_name": computer_name})
    else:
        send_data_to_firebase('/attack_results/T1649', {"output": output, "computer_name": computer_name})
    result_text.set("T1649 script executed")

def run_t1574():
    computer_name = get_computer_name()
    output, error = run_script('t1574_011.ps1')
    if error:
        send_data_to_firebase('/attack_results/T1574', {"output": error, "computer_name": computer_name})
    else:
        send_data_to_firebase('/attack_results/T1574', {"output": output, "computer_name": computer_name})
    result_text.set("T1574 script executed")

# GUI oluşturma
root = tk.Tk()
root.title("Mitre Attack Simulator")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

t1649_button = tk.Button(frame, text="Run T1649", command=run_t1649, padx=10, pady=5)
t1649_button.pack(side=tk.LEFT, padx=10)

t1574_button = tk.Button(frame, text="Run T1574", command=run_t1574, padx=10, pady=5)
t1574_button.pack(side=tk.LEFT, padx=10)

result_text = tk.StringVar()
result_label = tk.Label(frame, textvariable=result_text, pady=20)
result_label.pack()

root.mainloop()
