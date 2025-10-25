# Python program to print a line of text with each of the 8 Monokai colors on a normal background of (46, 46, 46)

# ANSI escape codes for setting text color
def ansi_color(rgb):
    return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"

# Monokai color scheme RGB values
colors = {
    "Comments": (121, 121, 121),
    "White": (214, 214, 214),
    "Yellow": (229, 181, 103),
    "Green": (180, 210, 115),
    "Orange": (232, 125, 62),
    "Purple": (158, 134, 200),
    "Pink": (176, 82, 121),
    "Blue": (108, 153, 187)
}

# Background color
background_color = "\033[48;2;46;46;46m"

# Reset color
reset_color = "\033[0m"

# Print text lines with each color
for color_name, rgb in colors.items():
    print(f"{background_color}{ansi_color(rgb)}{color_name}{reset_color}")

# Note: This script is designed to be run in a terminal that supports ANSI escape codes for 24-bit color.
# The colors will appear as intended if your terminal supports true color (24-bit color).

