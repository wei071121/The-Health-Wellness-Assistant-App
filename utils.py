import tkinter as tk

def clear_window(root):
    """Clear all widgets from the window"""
    for widget in root.winfo_children():
        widget.destroy()

def darken_color(hex_color, percent):
    """Darken a hex color by given percentage"""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    darkened = tuple(max(0, int(c * (1 - percent/100))) for c in rgb)
    return '#%02x%02x%02x' % darkened