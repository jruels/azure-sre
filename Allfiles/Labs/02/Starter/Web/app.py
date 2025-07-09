from flask import Flask, render_template, request, redirect, url_for, session
import requests
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace for production

# Hardcoded credentials
USERNAME = 'admin'
PASSWORD = 'password123'

# Your FastAPI backend base URL
BACKEND_API_BASE = os.environ.get('BACKEND_API_BASE', 'https://fallback-if-not-set')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if username == USERNAME and password == PASSWORD:
        session['user'] = username
        return redirect(url_for('dashboard'))
    return render_template('login.html', error='Invalid credentials')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/retrieve-price', methods=['GET', 'POST'])
def retrieve_price():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    result = None
    if request.method == 'POST':
        instrument_id = request.form['instrument_id']
        try:
            response = requests.get(f"{BACKEND_API_BASE}/api/retrieve-price", params={"symbol": instrument_id})
            result = response.json()
        except Exception as e:
            result = {"error": str(e)}
    return render_template('retrieve_price.html', result=result)

@app.route('/report-client-valuation', methods=['GET', 'POST'])
def report_client_valuation():
    if 'user' not in session:
        return redirect(url_for('login'))

    result = None
    if request.method == 'POST':
        client_id = request.form['client_id']
        valuation_data = request.form['valuation_data']
        try:
            payload = {"client_id": client_id, "valuation_data": valuation_data}
            response = requests.post(f"{BACKEND_API_BASE}/api/report-client-valuation", json=payload)
            result = response.json()
        except Exception as e:
            result = {"error": str(e)}
    return render_template('report_client_valuation.html', result=result)

@app.route('/delete-price', methods=['GET', 'POST'])
def delete_price():
    if 'user' not in session:
        return redirect(url_for('login'))

    result = None
    if request.method == 'POST':
        instrument_id = request.form['instrument_id']
        try:
            response = requests.delete(f"{BACKEND_API_BASE}/api/delete-price", params={"symbol": instrument_id})
            result = response.json()
        except Exception as e:
            result = {"error": str(e)}
    return render_template('delete_price.html', result=result)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
