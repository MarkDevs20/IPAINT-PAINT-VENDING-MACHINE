from customtkinter import CTkButton

class ColorButton(CTkButton):
    def __init__(self, parent, config, onToggle, **kwargs):
        self.colorName = config["name"]
        self.originalText = config["text"]
        self.originalColor = config["color"]
        self.originalTextColor = config.get("text_color", "#FFFFFF")
        self.hoverColor = config.get("hover", config["color"])
        self.onToggle = onToggle
        self.isSelected = False
        
        super().__init__(
            parent,
            text=self.originalText,
            font=("arial", 16, "bold"),
            width=130,
            height=80,
            corner_radius=12,
            fg_color=self.originalColor,
            hover_color=self.hoverColor,
            text_color=self.originalTextColor,
            command=self.handleClick,
            **kwargs
        )
    
    def handleClick(self):
        self.onToggle(self.colorName, self)
    
    def select(self):
        self.isSelected = True
        self.configure(text="SELECTED", fg_color="#32DC32")
    
    def deselect(self):
        self.isSelected = False
        self.configure(
            text=self.originalText,
            fg_color=self.originalColor,
            text_color=self.originalTextColor
        )
    
    def updateSize(self, width, height):
        self.configure(width=width, height=height)