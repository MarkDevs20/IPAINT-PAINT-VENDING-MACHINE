import firebase_admin
import json
import os
import urllib.request
from firebase_admin import credentials, db
from datetime import datetime

offlineFolder = "offlineData"
offLineOrdersFile = os.path.join(offlineFolder, "offLineOrders.json")
os.makedirs(offlineFolder, exist_ok=True)

try:
    app = firebase_admin.get_app('orderApp')
except ValueError:
    orderCred = credentials.Certificate(r'your own json file')
    app = firebase_admin.initialize_app(orderCred, {'databaseURL':'your own database url '})
    
def isConnected():
    try:
        urllib.request.urlopen('https://www.google.com', timeout=3)
        return True
    except:
        return False
    
def saveOrderLocalFile(order):
    orders = []
    if os.path.exists(offLineOrdersFile):
        with open(offLineOrdersFile, "r") as file:
            try:
                orders = json.load(file)
                if not isinstance(orders, list):
                    orders = []
            except json.JSONDecodeError:
                orders = []
    orders.append(order)
    with open(offLineOrdersFile, "w") as file:
        json.dump(orders, file, indent=4)
    print(f"Order saved in local file: {order}")

def uploadOfflineOrders():
    if not os.path.exists(offLineOrdersFile):
        return
    with open(offLineOrdersFile, "r") as file:
        try:
            orders = json.load(file)
            if not isinstance(orders, list):
                orders = []
        except json.JSONDecodeError:
            orders = []
    if not orders:
        return
    orderRef = db.reference('orderHistory', app=firebase_admin.get_app('orderApp'))
    for order in orders:
        newOrderRef = orderRef.push()
        newOrderRef.set(order)
    try:
        os.remove(offLineOrdersFile)
        print("Offline orders successfully uploaded and file removed.")
    except FileNotFoundError:
        print("Offline orders already removed or not found.")

def logOrder(color):
    timeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    orderData = {'color': color, 'time': timeStamp}
    if isConnected():
        orderRef = db.reference('orderHistory', app=firebase_admin.get_app('orderApp'))
        newOrderRef = orderRef.push()
        newOrderRef.set(orderData)
        print(f"Order logged: {orderData}")
    else:
        saveOrderLocalFile(orderData)
        print(f"Internet offline, order saved locally: {orderData}")