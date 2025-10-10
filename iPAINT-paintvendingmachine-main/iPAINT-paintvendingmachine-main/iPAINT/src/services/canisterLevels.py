import firebase_admin
import json
import os
import urllib.request
import threading
import time
from firebase_admin import credentials, db

offlineFolder = "offlineData"
offlinePaintFile = os.path.join(offlineFolder, "offlinePaintLevels.json")
os.makedirs(offlineFolder, exist_ok=True)

firebaseSync = False
offlineLock = threading.Lock()

def isConnected():
    try:
        urllib.request.urlopen("https://www.google.com", timeout=3)
        return True
    except:
        return False
    
def initializeFirebase():
    global firebaseSync
    if firebaseSync:
        return
    try:
        cred = credentials.Certificate(r'iPAINT/credentials/ipaintorderhistory-firebase-adminsdk-fbsvc-e00b549125.json')
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://ipaintorderhistory-default-rtdb.asia-southeast1.firebasedatabase.app/'})
        firebaseSync = True
        print("Firebase initialized for canisterLevels.")
    except Exception as e:
        print("initializeFirebase error (canisterLevels):", e)

def getPaintLevels():
    if isConnected():
        try:
            paintRef = db.reference('PaintLevels')
            return paintRef.get()
        except Exception as e:
            print("Error fetching paint levels from Firebase: ", e)
    if os.path.exists(offlinePaintFile):
        with offlineLock:
            try:
                with open(offlinePaintFile, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print("Error reading offline paint file: ", e)
                return {}
    return {}

def updatePaintLevels(color, amountUsedPercent):
    if isConnected():
        syncOfflinePaintLevels()
        try:
            ref = db.reference(f"PaintLevels/{color}/level")
            currentPercent = ref.get()
            if currentPercent is not None:
                newPercent = max(0, int(currentPercent) - amountUsedPercent)
                ref.set(newPercent)
                print(f"{color} updated to {newPercent}% (deducted {amountUsedPercent}%)")
            else:
                newPercent = max(0, 100 - amountUsedPercent)
                ref.set(newPercent)
                print(f"{color} missing in DB, initialized to {newPercent}%")
        except Exception as e:
            print("Error updating paint levels in Firebase:", e)
            _saveOfflinePaintUsage(color, amountUsedPercent)
    else:
        print(f"No internet! Storing {color} usage locally.")
        _saveOfflinePaintUsage(color, amountUsedPercent)

def _saveOfflinePaintUsage(color, amountUsed):
    with offlineLock:
        offlineData = {}
        if os.path.exists(offlinePaintFile):
            try:
                with open(offlinePaintFile, 'r') as f:
                    offlineData = json.load(f)
            except json.JSONDecodeError:
                offlineData = {}
            except Exception as e:
                print("Error reading offline paint file:", e)
                offlineData = {}
        offlineData[color] = offlineData.get(color, 0) + amountUsed
        try:
            with open(offlinePaintFile, 'w') as f:
                json.dump(offlineData, f, indent=4)
        except Exception as e:
            print("Error writing offline paint file:", e)

def syncOfflinePaintLevels():
    if not isConnected():
        return
    if not os.path.exists(offlinePaintFile):
        return
    with offlineLock:
        try:
            with open(offlinePaintFile, 'r') as f:
                try:
                    offlineData = json.load(f)
                except json.JSONDecodeError:
                    offlineData = {}
        except Exception as e:
            print("Error opening offline paint file for sync:", e)
            return
    if not offlineData:
        try:
            if os.path.exists(offlinePaintFile):
                os.remove(offlinePaintFile)
        except Exception as e:
            print("Error removing offline paint file:", e)
        return
    print("Syncing paint levels to Firebase...")

    try:
        for color, offlineUsed in offlineData.items():
            try:
                ref = db.reference(f'PaintLevels/{color}/level')
                currentPaintLevel = ref.get()
                if currentPaintLevel is None:
                    print(f"Color {color} not found in DB; initializing node.")
                    newLevel = max(0, 100 - offlineUsed)
                else:
                    newLevel = max(0, int(currentPaintLevel) - offlineUsed)
                ref.set(newLevel)
            except Exception as e:
                print(f"Error syncing color {color} to Firebase:", e)
        with offlineLock:
            if os.path.exists(offlinePaintFile):
                os.remove(offlinePaintFile)
        print("Sync complete for paint levels.")
    except Exception as e:
        print("Unexpected error during syncOfflinePaintLevels:", e)

def internetMonitoring():
    wasOffline = False
    while True:
        online = isConnected()
        if online and wasOffline:
            print("Internet reconnected! Syncing offline paint levels...")
            try:
                syncOfflinePaintLevels()
            except Exception as e:
                print("Error syncing after reconnect:", e)
        wasOffline = not online
        time.sleep(3)
initializeFirebase()