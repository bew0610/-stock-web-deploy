
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json, os
from utils import load_data, save_data, load_users, check_login, export_to_excel
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    data = load_data()
    return render_template('index.html', items=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_item():
    data = load_data()
    item = {
        "id": len(data) + 1,
        "name": request.form['name'],
        "sn": request.form['sn'],
        "qty": int(request.form['qty']),
        "unit": request.form['unit'],
        "history": [f"เพิ่ม {request.form['qty']} หน่วย ({datetime.now().strftime('%Y-%m-%d %H:%M')})"]
    }
    data.append(item)
    save_data(data)
    return redirect(url_for('home'))

@app.route('/export')
def export():
    export_to_excel()
    return jsonify({"message": "Exported to stock_report.xlsx"})

if __name__ == '__main__':
    app.run(debug=True)
