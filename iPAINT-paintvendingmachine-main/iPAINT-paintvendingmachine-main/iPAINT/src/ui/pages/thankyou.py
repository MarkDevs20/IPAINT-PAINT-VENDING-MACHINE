from customtkinter import CTkFrame, CTkLabel

class ThankYouFrame(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUI()
    
    def setupUI(self):
        self.thankYouLabel = CTkLabel(
            self, 
            text="THANK YOU FOR USING iPAINT", 
            font=("Arial", 30, "bold")
        )
        self.thankYouLabel.place(relx=0.5, rely=0.4, anchor="center")
        
        self.countdownLabel = CTkLabel(self, text="", font=("Arial", 25, "bold"))
        self.countdownLabel.place(relx=0.5, rely=0.5, anchor="center")
    
    def startCountdown(self, seconds, callback):
        self._countdown(seconds, callback)
    
    def _countdown(self, seconds, callback):
        if seconds > 0:
            self.countdownLabel.configure(text=f"Returning to Homepage in {seconds} seconds")
            self.after(1000, lambda: self._countdown(seconds - 1, callback))
        else:
            callback()