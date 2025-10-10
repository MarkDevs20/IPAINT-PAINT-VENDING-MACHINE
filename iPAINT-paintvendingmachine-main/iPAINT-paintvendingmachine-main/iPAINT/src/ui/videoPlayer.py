import cv2
from PIL import Image, ImageTk
from customtkinter import CTkLabel

class VideoPlayer:
    def __init__(self, parent, videoPath):
        self.parent = parent
        self.videoPath = videoPath
        self.cap = cv2.VideoCapture(self.videoPath)
        self.running = False
        self.videoLabel = CTkLabel(self.parent, text="")
        self.videoLabel.place(relx=0.5, rely=0.5, anchor="center")
        
    def playVideo(self):
        if not self.running:
            return
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (600, 400))
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            self.videoLabel.configure(image=img)
            self.videoLabel.image = img
            self.parent.after(30, self.playVideo)
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.playVideo()

    def start(self):
        self.running = True
        self.playVideo()

    def stop(self):
        self.running = False