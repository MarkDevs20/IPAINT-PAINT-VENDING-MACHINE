def getButtonSizes(screenWidth):
    if screenWidth < 1024:
        return {'color_width': 100, 'color_height': 60, 'main_width': 150, 'main_height': 50}
    elif screenWidth < 1440:
        return {'color_width': 130, 'color_height': 80, 'main_width': 200, 'main_height': 60}
    elif screenWidth < 1920:
        return {'color_width': 160, 'color_height': 100, 'main_width': 250, 'main_height': 70}
    else: 
        return {'color_width': 200, 'color_height': 120, 'main_width': 300, 'main_height': 80}