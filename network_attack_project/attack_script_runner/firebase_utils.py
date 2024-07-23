import firebase_admin
from firebase_admin import credentials, db
import logging
import os
from datetime import datetime

def initialize_firebase():
    try:
        # firebase_config.json dosyasının tam yolu
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'flask_app', 'firebase_config.json'))
        cred = credentials.Certificate(config_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://cyber-32dd2-default-rtdb.firebaseio.com/'
        })
        logging.info("Firebase initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing Firebase: {str(e)}")
        raise

def send_data_to_firebase(path, data):
    try:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        ref = db.reference(f"{path}/{timestamp}")
        ref.set(data)
        logging.info(f"Data sent to Firebase at {path}/{timestamp}: {data}")
    except Exception as e:
        logging.error(f"Error sending data to Firebase at {path}: {str(e)}")
