
import json
from openpyxl import Workbook

def load_data():
    try:
        with open('database.json', 'r') as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open('database.json', 'w') as f:
        json.dump(data, f, indent=2)

def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except:
        return {}

def check_login(username, password):
    users = load_users()
    return username in users and users[username] == password

def export_to_excel():
    data = load_data()
    wb = Workbook()
    ws = wb.active
    ws.append(["ID", "ชื่อสินค้า", "S/N", "จำนวน", "หน่วย", "ประวัติ"])
    for item in data:
        ws.append([item['id'], item['name'], item['sn'], item['qty'], item['unit'], " | ".join(item['history'])])
    wb.save("stock_report.xlsx")
