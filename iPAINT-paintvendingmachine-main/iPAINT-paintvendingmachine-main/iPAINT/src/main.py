import tkinter as CTk
import time
import ctypes
import sys
from customtkinter import CTk as CustomTk, set_appearance_mode
from datetime import datetime
from config.settings import *
from services.canisterLevels import getPaintLevels, updatePaintLevels, initializeFirebase
from services.orderHistory import logOrder, saveOrderLocalFile
from services.network import isConnected
from services.sync import SyncService
from hardware.serialConnection import SerialConnection
from ui.pages.homepage import HomeFrame
from ui.pages.colorselection import ColorSelectionFrame
from ui.pages.loading import LoadingFrame
from ui.pages.mix import MixFrame
from ui.pages.thankyou import ThankYouFrame
from utils.helpers import getButtonSizes

class iPaintApp:
    def __init__(self):
        self.app = None
        self.arduino = None
        self.syncService = None
        
        self.homeFrame = None
        self.colorSelectionFrame = None
        self.loadingFrame = None
        self.mixFrame = None
        self.thankYouFrame = None
        
        self.initializeApp()
    
    def initializeApp(self):
        if isConnected():
            initializeFirebase()
        
        self.syncService = SyncService(SYNC_INTERVAL)
        self.syncService.start()
        
        try:
            self.arduino = SerialConnection(baudRate=SERIAL_BAUDRATE, callback=self.serialCallback)
        except Exception as e:
            print(f"Error initializing Arduino: {e}")
            self.arduino = None
        
        self.setupWindow()
        self.setupFrames()
        
        self.app.bind('<Configure>', self.onWindowResize)
        self.app.after(500, self.updateButtonSizes)
        self.app.protocol("WM_DELETE_WINDOW", self.closeApp)
        
        self.showFrame(self.homeFrame)
    
    def setupWindow(self):
        if sys.platform.startswith("win"):
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u"iPAINT/assets/iPaintLogo.ico")
    
        self.app = CustomTk()
        self.app.title(APP_TITLE)
        self.app.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.app.minsize(APP_WIDTH, APP_HEIGHT)
        self.app.iconbitmap(APP_ICON)
        set_appearance_mode("dark")
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(0, weight=1)
        
        self.app.update_idletasks()
        screenWidth = self.app.winfo_screenwidth()
        screenHeight = self.app.winfo_screenheight()
        x = (screenWidth - APP_WIDTH) // 2
        y = (screenHeight - APP_HEIGHT) // 2
        self.app.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}")
    
    def setupFrames(self):
        # Home frame
        self.homeFrame = HomeFrame(self.app, self.onStartClicked)
        self.homeFrame.grid(row=0, column=0, sticky="nsew")
        
        # Color selection frame
        self.colorSelectionFrame = ColorSelectionFrame(
            self.app, 
            self.dispense, 
            lambda: self.showFrame(self.homeFrame)
        )
        self.colorSelectionFrame.grid(row=0, column=0, sticky="nsew")
        
        # Loading frame
        self.loadingFrame = LoadingFrame(self.app)
        self.loadingFrame.grid(row=0, column=0, sticky="nsew")
        
        # Mix frame
        self.mixFrame = MixFrame(self.app, self.mixPaint)
        self.mixFrame.grid(row=0, column=0, sticky="nsew")
        
        # Thank you frame
        self.thankYouFrame = ThankYouFrame(self.app)
        self.thankYouFrame.grid(row=0, column=0, sticky="nsew")
    
    def showFrame(self, frame):
        frame.tkraise()
        
        # Handle video player
        if frame == self.mixFrame:
            self.mixFrame.startVideo()
        else:
            self.mixFrame.stopVideo()
    
    def onStartClicked(self):
        self.colorSelectionFrame.resetButtons()
        self.colorSelectionFrame.selectedColor = None
        self.showFrame(self.colorSelectionFrame)
    
    def serialCallback(self, data):
        if data.isdigit():
            self.loadingFrame.setProgress(int(data) / 100)
            self.app.update()
        elif data == "DONE":
            time.sleep(1)
            self.showFrame(self.homeFrame)
    
    def dispense(self, selectedColor):
        self.loadingFrame.setText(f"DISPENSING YOUR PAINT PLEASE WAIT...")
        self.showFrame(self.loadingFrame)
        self.app.update()
        
        print(f"{selectedColor} MIXING STARTED")
        
        # Get command and paint amounts
        command = ARDUINO_COMMANDS.get(selectedColor)
        paintAmounts = PAINT_AMOUNTS.get(selectedColor, {})
        
        # Update paint levels
        for paintType, amount in paintAmounts.items():
            updatePaintLevels(paintType, amount)
        
        newLevel = getPaintLevels()
        print(f"Updated Paint levels: {newLevel}")
        
        # Log order
        if isConnected():
            logOrder(selectedColor)
        else:
            saveOrderLocalFile({
                'color': selectedColor, 
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            print(f"Offline: order saved {selectedColor} in local file")
        
        # Send command to Arduino
        if self.arduino and command:
            self.arduino.sendCommand(command)
            time.sleep(0.1)
            print(f"{selectedColor} MIXING STARTED")
            
            # Monitor progress
            while True:
                if self.arduino.serialPort.in_waiting > 0:
                    progress = self.arduino.serialPort.readline().decode().strip()
                    if progress.isdigit():
                        self.loadingFrame.setProgress(int(progress) / 100)
                        self.app.update()
                    elif progress == "DONE":
                        time.sleep(1)
                        self.showFrame(self.mixFrame)
                        break
    
    def mixPaint(self):
        self.loadingFrame.setText("MIXING YOUR PAINT\nPLEASE WAIT...")
        self.showFrame(self.loadingFrame)
        self.app.update()
        self.loadingFrame.setProgress(0)
        self.app.update()
        
        if self.arduino:
            self.arduino.sendCommand("C\n")
            self.arduino.serialPort.flush()
        
        # Progress animation
        for i in range(61):
            self.loadingFrame.setProgress(float(i) / 60)
            self.app.update()
            time.sleep(0.98)
        
        # Wait for Arduino confirmation
        if self.arduino:
            while True:
                if self.arduino.serialPort.in_waiting > 0:
                    response = self.arduino.serialPort.readline().decode().strip()
                    if response == "MIXING DONE":
                        break
        
        self.showThankYou()
    
    def showThankYou(self):
        self.showFrame(self.thankYouFrame)
        self.thankYouFrame.startCountdown(COUNTDOWN_SECONDS, lambda: self.showFrame(self.homeFrame))
    
    def updateButtonSizes(self):
        try:
            sizes = getButtonSizes(self.app.winfo_width())
            self.colorSelectionFrame.updateButtonSizes(sizes)
            self.mixFrame.updateButtonSizes(sizes)
        except:
            pass
    
    def onWindowResize(self, event):
        if event.widget == self.app:
            self.app.after(100, self.updateButtonSizes)
    
    def closeApp(self):
        if self.syncService:
            self.syncService.stop()
        if self.arduino and hasattr(self.arduino, 'stop'):
            self.arduino.stop()
        self.app.destroy()
    
    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = iPaintApp()
    app.run()