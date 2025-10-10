import threading
import time
from services.network import isConnected
from services.orderHistory import uploadOfflineOrders
from services.canisterLevels import syncOfflinePaintLevels

class SyncService:
    def __init__(self, interval=3):
        self.interval = interval
        self.running = False
        self.lock = threading.Lock()
        self.thread = None
    
    def start(self):
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._syncLoop, daemon=True)
        self.thread.start()
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
    
    def _syncLoop(self):
        while self.running:
            if isConnected():
                try:
                    uploadOfflineOrders()
                    syncOfflinePaintLevels()
                except Exception as e:
                    print(f"Sync error: {e}")
            time.sleep(self.interval)