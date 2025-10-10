from customtkinter import CTkFrame, CTkButton
from tkinter import PhotoImage, Label
from config.settings import APP_BACKGROUND

class HomeFrame(CTkFrame):
    def __init__(self, parent, onStart):
        super().__init__(parent)
        self.onStart = onStart
        self.setupUI()
    
    def setupUI(self):
        try:
            imagePath = PhotoImage(file=APP_BACKGROUND)
            bgImage = Label(self, image=imagePath)
            bgImage.image = imagePath  # Keep reference
            bgImage.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            pass
        
        self.startBtn = CTkButton(
            self, 
            text="START", 
            font=("Arial", 30, "bold"), 
            height=70, 
            corner_radius=0, 
            fg_color="#A020F0", 
            hover_color="#FFFFFF", 
            border_color="#000000", 
            border_width=2, 
            command=self.onStart
        )
        self.startBtn.place(relx=0.5, rely=0.965, anchor="center", relwidth=1)