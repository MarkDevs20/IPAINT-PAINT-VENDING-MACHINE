import tkinter as CTk
import time
import urllib.request
import threading
import ctypes
import sys
from customtkinter import*
from tkinter import PhotoImage, Label
from canisterLevels import getPaintLevels, updatePaintLevels, syncOfflinePaintLevels, initializeFirebase
from orderHistory import logOrder, uploadOfflineOrders, saveOrderLocalFile
from datetime import datetime
from serialConnection import SerialConnection
from videoPlayer import VideoPlayer

initializeFirebase()
def isConnected():
    try:
        urllib.request.urlopen('https://www.google.com', timeout=3)
        return True
    except:
        return False

if isConnected():
    initializeFirebase()

autoSync_running = threading.Lock()
def autoSync():
    if not autoSync_running.acquire(blocking=False):
        return  
    try:
        while True:
            if isConnected():
                uploadOfflineOrders()
                syncOfflinePaintLevels()
            time.sleep(3)
    finally:
        autoSync_running.release()

threading.Thread(target=autoSync, daemon=True).start()  

def serialCallback(data):
    if data.isdigit():
        progressBar.set(int(data) / 100)
        app.update()
    elif data == "DONE":
        time.sleep(1)
        showFrame(homePage)

try:
    arduino = SerialConnection(baudRate=115200, callback=serialCallback)
except Exception as e:
    print(f"Error: {e}")
    arduino = None

def showFrame(frame):
    frame.tkraise()

if sys.platform.startswith("win"):
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u"iPAINT/assets/iPaintLogo.ico")

app = CTk()
app.title("iPAINT - PAINT VENDING MACHINE")
app.geometry("1500x900")
app.minsize(1500, 900)
app.iconbitmap("iPAINT/assets/iPaintLogo.ico")
set_appearance_mode("dark")
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

def getButtonSizes():
    screen_width = app.winfo_width()
    if screen_width < 1024:
        return {'color_width': 100, 'color_height': 60, 'main_width': 150, 'main_height': 50}
    elif screen_width < 1440:
        return {'color_width': 130, 'color_height': 80, 'main_width': 200, 'main_height': 60}
    elif screen_width < 1920:
        return {'color_width': 160, 'color_height': 100, 'main_width': 250, 'main_height': 70}
    else: 
        return {'color_width': 200, 'color_height': 120, 'main_width': 300, 'main_height': 80}

def updateButtonSizes():
    try:
        sizes = getButtonSizes()
        
        permacoatBtn.configure(width=sizes['color_width'], height=sizes['color_height'])
        color1btn.configure(width=sizes['color_width'], height=sizes['color_height'])
        color2btn.configure(width=sizes['color_width'], height=sizes['color_height'])
        color3btn.configure(width=sizes['color_width'], height=sizes['color_height'])
        color4btn.configure(width=sizes['color_width'], height=sizes['color_height'])
        color5btn.configure(width=sizes['color_width'], height=sizes['color_height'])
        color6btn.configure(width=sizes['color_width'], height=sizes['color_height'])
        color7btn.configure(width=sizes['color_width'], height=sizes['color_height'])
        color8btn.configure(width=sizes['color_width'], height=sizes['color_height'])
        color9btn.configure(width=sizes['color_width'], height=sizes['color_height'])
        color10btn.configure(width=sizes['color_width'], height=sizes['color_height'])
        
        dispenseBtn.configure(width=sizes['main_width'], height=sizes['main_height'])
        mixBtn.configure(width=sizes['main_width'], height=sizes['main_height'])
        
        cancelBtn.configure(width=sizes['main_width'], height=sizes['main_height'])
        
    except:
        pass

homePage = CTkFrame(app)
homePage.grid(row=0, column=0, sticky="nsew")

try:
    imagePath = PhotoImage(file="iPAINT/assets/i (900 x 600 px).png")
    bgImage = Label(homePage, image=imagePath)
    bgImage.place(x=0, y=0, relwidth=1, relheight=1)
except:
    pass

startBtn = CTkButton(homePage, text="START", font=("Arial", 30, "bold"), height=70, corner_radius=0, fg_color="#A020F0", hover_color="#FFFFFF", border_color="#000000", border_width=2, command=lambda: showFrame(colorSelection))
startBtn.place(relx=0.5, rely=0.965, anchor="center", relwidth=1)

colorSelection = CTkFrame(app)
colorSelection.grid(row=0, column=0, sticky="nsew")

colorLabel = CTkLabel(colorSelection, text="COLOR SELECTION", font=("Arial", 50, "bold"))
colorLabel.place(relx=0.5, rely=0.1, anchor="n")

outlineBox = CTkFrame(colorSelection, fg_color=("#FFFFFF", "#2a2a2a"), border_width=2, border_color=("#e2e8f0", "#4a5568"), corner_radius=20)
outlineBox.place(relx=0.5, rely=0.51, anchor="center", relwidth=0.75, relheight=0.6)

selectedColor = None

def toggleColor(colorName, button):
    global selectedColor
    if selectedColor == colorName:
        resetButtons()
        selectedColor = None
    else:
        resetButtons()
        button.configure(text="SELECTED", fg_color="#32DC32")
        selectedColor = colorName

def resetButtons():
    permacoatBtn.configure(text="PERMACOAT", fg_color="#FFFFFF")
    color1btn.configure(text="CORNFLOWER\nBLUE\n#6395EE", fg_color="#6395EE", text_color="white", hover_color="#5a8de6")
    color2btn.configure(text="MAIZE\n#FBEC5D", fg_color="#FBEC5D")
    color3btn.configure(text="TURQUOISE\n#40E0D0",  fg_color="#40E0D0")
    color4btn.configure(text="PALE VIOLET\nRED\n#DB7093", fg_color="#DB7093")
    color5btn.configure(text="COLOR5\n#FFFFFF", fg_color="#FFFFFF")
    color6btn.configure(text="COLOR6\n#FFFFFF", fg_color="#FFFFFF")
    color7btn.configure(text="COLOR7\n#FFFFFF", fg_color="#FFFFFF")
    color8btn.configure(text="COLOR8\n#FFFFFF", fg_color="#FFFFFF")
    color9btn.configure(text="COLOR9\n#FFFFFF", fg_color="#FFFFFF")
    color10btn.configure(text="COLOR10\n#FFFFFF", fg_color="#FFFFFF")

buttonWidth = 130
buttonHeight = 80

permacoatBtn = CTkButton(colorSelection, text="PERMACOAT", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#FFFFFF", hover_color="#FFFFFF",text_color="#000000",command=lambda: toggleColor("PERMACOAT", permacoatBtn))
permacoatBtn.place(relx=0.20, rely=0.31, anchor="center")

color1btn = CTkButton(colorSelection, text="CORNFLOWER\nBLUE\n#6395EE", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12 ,fg_color="#6395EE", hover_color="#0c5ce7", text_color="#FFFFFF",command=lambda: toggleColor("CORNFLOWER BLUE", color1btn))
color1btn.place(relx=0.32, rely=0.31, anchor="center")

color2btn = CTkButton(colorSelection, text="MAIZE\nYELLOW\n#FBEC5D", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#FBEC5D", hover_color="#ecd60b", text_color="#FFFFFF" ,command=lambda: toggleColor("MAIZE", color2btn))
color2btn.place(relx=0.44, rely=0.31, anchor="center")

color3btn = CTkButton(colorSelection, text="TURQUOISE\n#40E0D0", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#40E0D0", hover_color="#07f5dd", text_color="#FFFFFF" ,command=lambda: toggleColor("TURQUOISE", color3btn))
color3btn.place(relx=0.56, rely=0.31, anchor="center")

color4btn = CTkButton(colorSelection, text="PALEVIOLET\nRED\n#DB7093", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#DB7093", hover_color="#d6648a", text_color="#FFFFFF" ,command=lambda: toggleColor("PALE VIOLETRED", color4btn))
color4btn.place(relx=0.68, rely=0.31, anchor="center")

color5btn = CTkButton(colorSelection, text="COLOR5\n#FFFFFF", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#FFFFFF", hover_color="#FFFFFF",text_color="#000000",command=lambda: toggleColor("COLOR5", color5btn))
color5btn.place(relx=0.80, rely=0.31, anchor="center")

color6btn =CTkButton(colorSelection, text="COLOR6\n#FFFFFF", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#FFFFFF", hover_color="#FFFFFF",text_color="#000000",command=lambda: toggleColor("COLOR6", color6btn))
color6btn.place(relx=0.20, rely=0.46, anchor="center")

color7btn = CTkButton(colorSelection, text="COLOR7\n#FFFFFF", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#FFFFFF", hover_color="#FFFFFF",text_color="#000000",command=lambda: toggleColor("COLOR7", color7btn))
color7btn.place(relx=0.32, rely=0.46, anchor="center")

color8btn = CTkButton(colorSelection, text="COLOR8\n#FFFFFF", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#FFFFFF", hover_color="#FFFFFF",text_color="#000000",command=lambda: toggleColor("COLOR8", color8btn))
color8btn.place(relx=0.44, rely=0.46, anchor="center")

color9btn = CTkButton(colorSelection, text="COLOR9\n#FFFFFF", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#FFFFFF", hover_color="#FFFFFF",text_color="#000000",command=lambda: toggleColor("COLOR9", color9btn))
color9btn.place(relx=0.56, rely=0.46, anchor="center")

color10btn = CTkButton(colorSelection, text="COLOR10\n#FFFFFF", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#FFFFFF", hover_color="#FFFFFF",text_color="#000000",command=lambda: toggleColor("COLOR10", color10btn))
color10btn.place(relx=0.68, rely=0.46, anchor="center")

cancelBtn = CTkButton(colorSelection, text="CANCEL", font=("Arial", 30, "bold"), width=200, height=60, fg_color="#F72B07", hover_color="#FF6347", command=lambda: showFrame(homePage))
cancelBtn.place(relx=0.21, rely=0.9, anchor= "center" )

dispenseBtn = CTkButton(colorSelection, text="DISPENSE", font=("Arial", 30, "bold"), width=200, height=60, fg_color="#08f33f", hover_color="#34d058" , command=lambda: dispense())
dispenseBtn.place(relx=0.79, rely=0.9, anchor="center")

loadingScreen = CTkFrame(app)
loadingScreen.grid(row=0, column=0, sticky="nsew")

loadingLabel = CTkLabel(loadingScreen, text="DISPENSING PAINT", font=("Arial", 30, "bold"))
loadingLabel.place(relx=0.5, rely=0.42, anchor="center")

progressBar = CTkProgressBar(loadingScreen, height=50, corner_radius=25, fg_color=("#e9ecef", "#4a5568"), progress_color=("#28a745", "#34d058"))
progressBar.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5)
progressBar.set(0)

def dispense():
    if selectedColor:
        loadingLabel.configure(text=f"DISPENSING YOUR PAINT PLEASE WAIT...")
        showFrame(loadingScreen)
        app.update()
        print(f"{selectedColor} MIXING STARTED")
        
        if selectedColor == "PERMACOAT":
            command = "P\n"
            updatePaintLevels("permacoat", 14)
        elif selectedColor == "CORNFLOWER BLUE":
            command = "1\n"
            updatePaintLevels("permacoat", 14)
            updatePaintLevels("blue", 6)
        elif selectedColor == "MAIZE":
            command = "2\n"
            updatePaintLevels("permacoat", 14)
            updatePaintLevels("yellow", 6)
        elif selectedColor == "TURQUOISE":
            command = "3\n"
            updatePaintLevels("permacoat", 14)
            updatePaintLevels("green", 6)
        elif selectedColor == "PALE VIOLETRED":
            command = "4\n"
            updatePaintLevels("permacoat", 14)
            updatePaintLevels("red", 6)
        elif selectedColor == "COLOR5":
            command = "5\n"
            updatePaintLevels("permacoat", 14)
            updatePaintLevels("blue", 3)
            updatePaintLevels("yellow", 3)
        elif selectedColor == "COLOR6":
            command = "6\n"
            updatePaintLevels("permacoat", 14)
            updatePaintLevels("green", 3)
            updatePaintLevels("red", 3)
        elif selectedColor == "COLOR7":
            command = "7\n"
            updatePaintLevels("permacoat", 14)
            updatePaintLevels("yellow", 3)
            updatePaintLevels("green", 3)
        elif selectedColor == "COLOR8":
            command = "8\n"
            updatePaintLevels("permacoat", 14)
            updatePaintLevels("blue", 3)
            updatePaintLevels("red", 3)
        elif selectedColor == "COLOR9":
            command = "9\n"
            updatePaintLevels("permacoat", 14)
            updatePaintLevels("yellow", 3)
            updatePaintLevels("red", 3)
        elif selectedColor == "COLOR10":
            command = "C10\n"
            updatePaintLevels("permacoat", 14)
            updatePaintLevels("blue", 3)
            updatePaintLevels("green", 3)
            
        newLevel = getPaintLevels()
        print(f"Updated Paint levels: {newLevel}")
        
        if isConnected():
            logOrder(selectedColor)
        else:
            saveOrderLocalFile({'color': selectedColor, 'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            print(f"Offline: order saved {selectedColor} in local file")
            
        if arduino:
            arduino.sendCommand(command)
            time.sleep(0.1)
            print(f"{selectedColor} MIXING STARTED")
            
            while True:
                if arduino.serialPort.in_waiting > 0:
                    progress = arduino.serialPort.readline().decode().strip()
                    if progress.isdigit():
                        progressBar.set(int(progress) / 100)
                        app.update()
                    elif progress == "DONE":
                        time.sleep(1)
                        showFrame(compressAndShake)
                        break
    else:
        notificationLabel = CTkLabel(colorSelection, text="Select a color first", font=("Arial", 20, "bold"), text_color="#FFFFFF", width=130, height=80, corner_radius=12, fg_color="#B22222")
        notificationLabel.place(relx=0.5, rely=0.500, anchor="center")
        app.after(2000, notificationLabel.destroy)

compressAndShake = CTkFrame(app)
compressAndShake.grid(row=0, column=0, sticky="nsew")
try:
    videoPlayer = VideoPlayer(compressAndShake, "video.mp4")
except:
    pass
instructionLabel = CTkLabel(compressAndShake, text="PLEASE PLACE THE LID ON THE BUCKET\nTHEN PRESS THE MIX BUTTON", font=("Arial", 30, "bold"), justify="center")
instructionLabel.place(relx=0.5, rely=0.1, anchor="center")
mixBtn = CTkButton(compressAndShake, text="MIX", font=("Arial", 25, "bold"), width=200, height=60, fg_color="#32CD32", hover_color="#228B22", command=lambda: mixPaint())
mixBtn.place(relx=0.5, rely=0.9, anchor="center")

def showMixFrame(frame):
    frame.tkraise()
    if frame == compressAndShake:
        try:
            videoPlayer.start()
        except:
            pass
    else:
        try:
            videoPlayer.stop()
        except:
            pass

def mixPaint():
    loadingLabel.configure(text="MIXING YOUR PAINT\nPLEASE WAIT...")
    showFrame(loadingScreen)
    app.update()
    progressBar.set(0)
    app.update()
    
    if arduino:
        arduino.sendCommand("C\n")
        arduino.serialPort.flush()
    for i in range(61):
        progressBar.set(float(i) / 60)
        app.update()
        time.sleep(0.98)
    if arduino:
        while True:
            if arduino.serialPort.in_waiting > 0:
                response = arduino.serialPort.readline().decode().strip()
                if response == "MIXING DONE":
                    break
    showThankYou()

thankYou = CTkFrame(app)
thankYou.grid(row=0, column=0, sticky="nsew")

thankYouLabel = CTkLabel(thankYou, text="THANK YOU FOR USING iPAINT", font=("Arial", 30, "bold"))
thankYouLabel.place(relx=0.5, rely=0.4, anchor="center")

countdownLabel = CTkLabel(thankYou, text="", font=("Arial", 25, "bold"))
countdownLabel.place(relx=0.5, rely=0.5, anchor="center")

def countdown(seconds):
    if seconds > 0:
        countdownLabel.configure(text=f"Returning to Homepage in {seconds} seconds")
        app.after(1000, countdown, seconds - 1)
    else:
        showFrame(homePage)

def showThankYou():
    showFrame(thankYou)
    countdown(15)    

def onWindowResize(event):
    if event.widget == app:
        app.after(100, updateButtonSizes)  

app.bind('<Configure>', onWindowResize)
app.after(500, updateButtonSizes)

def closeApp():
    global arduino
    if arduino and hasattr(arduino, 'stop'):
        arduino.stop()
    app.destroy()

app.protocol("WM_DELETE_WINDOW", closeApp)
showFrame(homePage)
app.mainloop()