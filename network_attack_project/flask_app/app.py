from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate('../flask_app/firebase_config.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cyber-32dd2-default-rtdb.firebaseio.com/'
})

def format_timestamp(timestamp):
    dt = datetime.strptime(timestamp, '%Y%m%d%H%M%S')
    return dt.strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
    t1649_ref = db.reference('/attack_results/T1649')
    t1574_ref = db.reference('/attack_results/T1574')
    
    t1649_results = t1649_ref.order_by_key().get()
    t1574_results = t1574_ref.order_by_key().get()

    # Sonuçları tersine çevir ve zaman damgalarını formatla
    t1649_results = {format_timestamp(k): v for k, v in sorted(t1649_results.items(), reverse=True)} if t1649_results else {}
    t1574_results = {format_timestamp(k): v for k, v in sorted(t1574_results.items(), reverse=True)} if t1574_results else {}
    
    return render_template('index.html', t1649_results=t1649_results, t1574_results=t1574_results)

if __name__ == '__main__':
    app.run(debug=True)


