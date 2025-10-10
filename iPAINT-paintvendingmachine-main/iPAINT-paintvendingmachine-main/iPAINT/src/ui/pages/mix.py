from customtkinter import CTkFrame, CTkLabel, CTkButton
from ui.videoPlayer import VideoPlayer
from config.settings import APP_VIDEO

class MixFrame(CTkFrame):
    def __init__(self, parent, onMix):
        super().__init__(parent)
        self.onMix = onMix
        self.videoPlayer = None
        self.setupUI()
    
    def setupUI(self):
        try:
            self.videoPlayer = VideoPlayer(self, APP_VIDEO)
        except:
            pass
        
        instructionLabel = CTkLabel(
            self, 
            text="PLEASE PLACE THE LID ON THE BUCKET\nTHEN PRESS THE MIX BUTTON", 
            font=("Arial", 30, "bold"), 
            justify="center"
        )
        instructionLabel.place(relx=0.5, rely=0.1, anchor="center")
        
        self.mixBtn = CTkButton(
            self, 
            text="MIX", 
            font=("Arial", 25, "bold"), 
            width=200, 
            height=60, 
            fg_color="#32CD32", 
            hover_color="#228B22", 
            command=self.onMix
        )
        self.mixBtn.place(relx=0.5, rely=0.9, anchor="center")
    
    def startVideo(self):
        if self.videoPlayer:
            try:
                self.videoPlayer.start()
            except:
                pass
    
    def stopVideo(self):
        if self.videoPlayer:
            try:
                self.videoPlayer.stop()
            except:
                pass
    
    def updateButtonSizes(self, sizes):
        self.mixBtn.configure(width=sizes['main_width'], height=sizes['main_height'])