import os

# Application settings
APP_TITLE = "iPAINT - PAINT VENDING MACHINE"
APP_WIDTH = 1500
APP_HEIGHT = 900
APP_ICON = "iPAINT/assets/iPaintLogo.ico"
APP_BACKGROUND = "iPAINT/assets/i (900 x 600 px).png"
APP_VIDEO = "iPAINT/assets/video.mp4"

# Serial settings
SERIAL_BAUDRATE = 115200

# Paint levels (in ounces)
PAINT_AMOUNTS = {
    "PERMACOAT": {"permacoat": 14},
    "CORNFLOWER BLUE": {"permacoat": 14, "blue": 6},
    "MAIZE": {"permacoat": 14, "yellow": 6},
    "TURQUOISE": {"permacoat": 14, "green": 6},
    "PALE VIOLETRED": {"permacoat": 14, "red": 6},
    "COLOR5": {"permacoat": 14, "blue": 3, "yellow": 3},
    "COLOR6": {"permacoat": 14, "green": 3, "red": 3},
    "COLOR7": {"permacoat": 14, "yellow": 3, "green": 3},
    "COLOR8": {"permacoat": 14, "blue": 3, "red": 3},
    "COLOR9": {"permacoat": 14, "yellow": 3, "red": 3},
    "COLOR10": {"permacoat": 14, "blue": 3, "green": 3}
}

# Arduino commands
ARDUINO_COMMANDS = {
    "PERMACOAT": "P\n",
    "CORNFLOWER BLUE": "1\n",
    "MAIZE": "2\n",
    "TURQUOISE": "3\n",
    "PALE VIOLETRED": "4\n",
    "COLOR5": "5\n",
    "COLOR6": "6\n",
    "COLOR7": "7\n",
    "COLOR8": "8\n",
    "COLOR9": "9\n",
    "COLOR10": "C10\n"
}

# Color button configurations
COLOR_BUTTONS = [
    {"name": "PERMACOAT", "text": "PERMACOAT", "color": "#FFFFFF", "text_color": "#000000"},
    {"name": "CORNFLOWER BLUE", "text": "CORNFLOWER\nBLUE\n#6395EE", "color": "#6395EE", "text_color": "#FFFFFF", "hover": "#5a8de6"},
    {"name": "MAIZE", "text": "MAIZE\n#FBEC5D", "color": "#FBEC5D", "text_color": "#000000", "hover": "#ecd60b"},
    {"name": "TURQUOISE", "text": "TURQUOISE\n#40E0D0", "color": "#40E0D0", "text_color": "#FFFFFF", "hover": "#07f5dd"},
    {"name": "PALE VIOLETRED", "text": "PALEVIOLET\nRED\n#DB7093", "color": "#DB7093", "text_color": "#FFFFFF", "hover": "#d6648a"},
    {"name": "COLOR5", "text": "COLOR5\n#FFFFFF", "color": "#FFFFFF", "text_color": "#000000"},
    {"name": "COLOR6", "text": "COLOR6\n#FFFFFF", "color": "#FFFFFF", "text_color": "#000000"},
    {"name": "COLOR7", "text": "COLOR7\n#FFFFFF", "color": "#FFFFFF", "text_color": "#000000"},
    {"name": "COLOR8", "text": "COLOR8\n#FFFFFF", "color": "#FFFFFF", "text_color": "#000000"},
    {"name": "COLOR9", "text": "COLOR9\n#FFFFFF", "color": "#FFFFFF", "text_color": "#000000"},
    {"name": "COLOR10", "text": "COLOR10\n#FFFFFF", "color": "#FFFFFF", "text_color": "#000000"}
]

# Sync settings
SYNC_INTERVAL = 3  # seconds
COUNTDOWN_SECONDS = 15
MIX_DURATION = 60  # second