from customtkinter import CTkFrame, CTkLabel, CTkProgressBar

class LoadingFrame(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUI()
    
    def setupUI(self):
        self.loadingLabel = CTkLabel(self, text="DISPENSING PAINT", font=("Arial", 30, "bold"))
        self.loadingLabel.place(relx=0.5, rely=0.42, anchor="center")
        
        self.progressBar = CTkProgressBar(
            self, 
            height=50, 
            corner_radius=25, 
            fg_color=("#e9ecef", "#4a5568"), 
            progress_color=("#28a745", "#34d058")
        )
        self.progressBar.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5)
        self.progressBar.set(0)
    
    def setProgress(self, value):
        self.progressBar.set(value)
    
    def setText(self, text):
        self.loadingLabel.configure(text=text)