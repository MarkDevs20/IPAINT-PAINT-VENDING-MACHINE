from customtkinter import CTkFrame, CTkLabel, CTkButton

class ColorSelectionFrame(CTkFrame):
    def __init__(self, parent, onDispense, onCancel):
        super().__init__(parent)
        self.onDispense = onDispense
        self.onCancel = onCancel
        self.selectedColor = None
        self.setupUI()
        self.bind("<Configure>", self.onResize)
    
    def setupUI(self):
        self.colorLabel = CTkLabel(self, text="COLOR SELECTION", font=("Arial", 50, "bold"))
        self.colorLabel.place(relx=0.5, rely=0.1, anchor="n")
        
        self.outlineBox = CTkFrame(
            self, 
            fg_color=("#FFFFFF", "#2a2a2a"), 
            border_width=2, 
            border_color=("#e2e8f0", "#4a5568"), 
            corner_radius=20
        )
        self.outlineBox.place(relx=0.5, rely=0.51, anchor="center", relwidth=0.75, relheight=0.6)
        
        buttonWidth = 130
        buttonHeight = 80
        
        self.permacoatBtn = CTkButton(self, text="PERMACOAT", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#FFFFFF", hover_color="#FFFFFF", text_color="#000000", command=lambda: self.toggleColor("PERMACOAT", self.permacoatBtn))
        
        self.color1btn = CTkButton(self, text="CORNFLOWER\nBLUE\n#6395EE", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#6395EE", hover_color="#0c5ce7", text_color="#FFFFFF", command=lambda: self.toggleColor("CORNFLOWER BLUE", self.color1btn))
        
        self.color2btn = CTkButton(self, text="MAIZE\nYELLOW\n#FBEC5D", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#FBEC5D", hover_color="#ecd60b", text_color="#FFFFFF", command=lambda: self.toggleColor("MAIZE", self.color2btn))
        
        self.color3btn = CTkButton(self, text="TURQUOISE\n#40E0D0", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#40E0D0", hover_color="#07f5dd", text_color="#FFFFFF", command=lambda: self.toggleColor("TURQUOISE", self.color3btn))
        
        self.color4btn = CTkButton(self, text="PALEVIOLET\nRED\n#DB7093", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#DB7093", hover_color="#d6648a", text_color="#FFFFFF", command=lambda: self.toggleColor("PALE VIOLETRED", self.color4btn))
        
        self.color5btn = CTkButton(self, text="COLOR5\n#FFFFFF", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#FFFFFF", hover_color="#FFFFFF", text_color="#000000", command=lambda: self.toggleColor("COLOR5", self.color5btn))
        
        self.color6btn = CTkButton(self, text="COLOR6\n#FFFFFF", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#FFFFFF", hover_color="#FFFFFF", text_color="#000000", command=lambda: self.toggleColor("COLOR6", self.color6btn))
        
        self.color7btn = CTkButton(self, text="COLOR7\n#FFFFFF", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#FFFFFF", hover_color="#FFFFFF", text_color="#000000", command=lambda: self.toggleColor("COLOR7", self.color7btn))
        
        self.color8btn = CTkButton(self, text="COLOR8\n#FFFFFF", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#FFFFFF", hover_color="#FFFFFF", text_color="#000000", command=lambda: self.toggleColor("COLOR8", self.color8btn))
        
        self.color9btn = CTkButton(self, text="COLOR9\n#FFFFFF", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#FFFFFF", hover_color="#FFFFFF", text_color="#000000", command=lambda: self.toggleColor("COLOR9", self.color9btn))
        
        self.color10btn = CTkButton(self, text="COLOR10\n#FFFFFF", font=("arial", 16, "bold"), width=buttonWidth, height=buttonHeight, corner_radius=12, fg_color="#FFFFFF", hover_color="#FFFFFF", text_color="#000000", command=lambda: self.toggleColor("COLOR10", self.color10btn))
        
        self.colorButtons = [
            self.permacoatBtn, self.color1btn, self.color2btn, self.color3btn, 
            self.color4btn, self.color5btn, self.color6btn, self.color7btn, 
            self.color8btn, self.color9btn, self.color10btn
        ]
        
        # Cancel button
        self.cancelBtn = CTkButton(self, text="CANCEL", font=("Arial", 30, "bold"), width=200, height=60, fg_color="#F72B07", hover_color="#FF6347", command=self.onCancel)
        self.cancelBtn.place(relx=0.21, rely=0.9, anchor="center")
        
        # Dispense button
        self.dispenseBtn = CTkButton(self, text="DISPENSE", font=("Arial", 30, "bold"), width=200, height=60, fg_color="#08f33f", hover_color="#34d058", command=self.handleDispense)
        self.dispenseBtn.place(relx=0.79, rely=0.9, anchor="center")
        
        # Initial positioning
        self.positionButtons()
    
    def positionButtons(self):
        screenWidth = self.winfo_width()
        
        if screenWidth < 1024:
            row1_positions = [0.18, 0.30, 0.42, 0.54, 0.66, 0.78]
            row2_positions = [0.18, 0.30, 0.42, 0.54, 0.66]
        elif screenWidth < 1440:
            row1_positions = [0.19, 0.31, 0.43, 0.55, 0.67, 0.79]
            row2_positions = [0.19, 0.31, 0.43, 0.55, 0.67]
        else:
            row1_positions = [0.20, 0.32, 0.44, 0.56, 0.68, 0.80]
            row2_positions = [0.20, 0.32, 0.44, 0.56, 0.68]
        
        for i in range(6):
            self.colorButtons[i].place(relx=row1_positions[i], rely=0.31, anchor="center")
        
        for i in range(5):
            self.colorButtons[i + 6].place(relx=row2_positions[i], rely=0.46, anchor="center")
    
    def onResize(self, event):
        if event:
            self.after(10, self.positionButtons)
    
    def toggleColor(self, colorName, button):
        if self.selectedColor == colorName:
            self.resetButtons()
            self.selectedColor = None
        else:
            self.resetButtons()
            button.configure(text="SELECTED", fg_color="#32DC32")
            self.selectedColor = colorName
    
    def resetButtons(self):
        self.permacoatBtn.configure(text="PERMACOAT", fg_color="#FFFFFF")
        self.color1btn.configure(text="CORNFLOWER\nBLUE\n#6395EE", fg_color="#6395EE", text_color="white", hover_color="#5a8de6")
        self.color2btn.configure(text="MAIZE\nYELLOW\n#FBEC5D", fg_color="#FBEC5D")
        self.color3btn.configure(text="TURQUOISE\n#40E0D0", fg_color="#40E0D0")
        self.color4btn.configure(text="PALEVIOLET\nRED\n#DB7093", fg_color="#DB7093")
        self.color5btn.configure(text="COLOR5\n#FFFFFF", fg_color="#FFFFFF")
        self.color6btn.configure(text="COLOR6\n#FFFFFF", fg_color="#FFFFFF")
        self.color7btn.configure(text="COLOR7\n#FFFFFF", fg_color="#FFFFFF")
        self.color8btn.configure(text="COLOR8\n#FFFFFF", fg_color="#FFFFFF")
        self.color9btn.configure(text="COLOR9\n#FFFFFF", fg_color="#FFFFFF")
        self.color10btn.configure(text="COLOR10\n#FFFFFF", fg_color="#FFFFFF")
    
    def handleDispense(self):
        if self.selectedColor:
            self.onDispense(self.selectedColor)
        else:
            self.showNotification("Select a color first")
    
    def showNotification(self, message):
        notificationLabel = CTkLabel(
            self, 
            text=message, 
            font=("Arial", 20, "bold"), 
            text_color="#FFFFFF", 
            width=130, 
            height=80, 
            corner_radius=12, 
            fg_color="#B22222"
        )
        notificationLabel.place(relx=0.5, rely=0.500, anchor="center")
        self.after(2000, notificationLabel.destroy)
    
    def updateButtonSizes(self, sizes):
        self.permacoatBtn.configure(width=sizes['color_width'], height=sizes['color_height'])
        self.color1btn.configure(width=sizes['color_width'], height=sizes['color_height'])
        self.color2btn.configure(width=sizes['color_width'], height=sizes['color_height'])
        self.color3btn.configure(width=sizes['color_width'], height=sizes['color_height'])
        self.color4btn.configure(width=sizes['color_width'], height=sizes['color_height'])
        self.color5btn.configure(width=sizes['color_width'], height=sizes['color_height'])
        self.color6btn.configure(width=sizes['color_width'], height=sizes['color_height'])
        self.color7btn.configure(width=sizes['color_width'], height=sizes['color_height'])
        self.color8btn.configure(width=sizes['color_width'], height=sizes['color_height'])
        self.color9btn.configure(width=sizes['color_width'], height=sizes['color_height'])
        self.color10btn.configure(width=sizes['color_width'], height=sizes['color_height'])
        self.cancelBtn.configure(width=sizes['main_width'], height=sizes['main_height'])
        self.dispenseBtn.configure(width=sizes['main_width'], height=sizes['main_height'])