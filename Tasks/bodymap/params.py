"""Miscellaneous definitions of parameters used to set the beavhior of the
experiment. Mostly visual characteristics - size, color, position, etc.
"""
import numpy as np
import ctypes

user32 = ctypes.windll.user32
SCREEN_SIZE = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# for debugging
END_EXP_KEY = 'q'

# Used to correct, as monitor is rectengular and not square.
EXPECTED_MONITOR_RESOLUTION = np.array([1, SCREEN_SIZE[0] / SCREEN_SIZE[1]])

# Control whether including outer body lines inside the perimeter of a dot
# is permitted or prohibited. True allows coloring over body lines.
ALLOW_DRAWING_ON_LINES = True

# Whether you can hold down a key for 'semi-continuous' drawing
ALLOW_CONTINUOUS_DRAWING = False

# The n-back actions you can cancel. 0 or higher, an integer.
UNDO_NUM = 3

# Disable Undo button (set to True in case you want the undo functionality)
ENABLE_UNDO = True

# Sets the color of the cursor  (opposed)
ERASER_OFF_COLOR = 'black'
ERASER_ON_COLOR = 'red'

# Sets the color of the eraser frame (opposed)
ERASER_FRAME_OFF_COLOR = 'green'
ERASER_FRAME_ON_COLOR = 'red'

ERASER_FRAME_SIZE = 170
# How long to delay a second check of the mouse button
# status following a 'button down' result
WAIT_PERIOD = 0.1

# The color of the drawn contours on the contour-finding process
CONTOUR_COLOR = [0, 255, 0]
# Used to set the number of pixels cropped from the frame surrounding the
# image, which is detected as contour, although it is in truth far from the
# silhouette.
CLIPPING_SIZE = 8

DOT_RADIUS: int = 10  # In pixels
DOT_LINE_WIDTH = 3  # In pixels
DOT_COLOR = 'grey'
DOT_ALPHA = 0.15  # Initial value of sensation transparency
TONE_MB_LEFT = 'red'  # 'Hedonic' color for left-click
TONE_MB_RIGHT = 'blue'  # 'Hedonic' color for left-click

# 5 possible values of sensation transparency
DOT_ALPHA_INTENSITIES = np.linspace(DOT_ALPHA, 1, 5)

# ------------------------------------------------------------------------------
# NB! Some values of the IMG_SIZE factor may not work and lead to no drawing
# area being recognized or flowing out of the scene (pending screen resolution).
# To match the illustrations on the instructions, use ~0.33.
# Best values would be 0.38, as they are recognized well both on standard
# (1920X1080 @ 125%) or unique displays (1280 X 1024 @ 100%).
# The image resolution is roughly 1:1.41, but screen resolution is 1:1.77
IMG_SIZE = EXPECTED_MONITOR_RESOLUTION * np.array([1, 3508 / 2481]) * 0.38
# ------------------------------------------------------------------------------


# Cursor marker height
CURSOR_MARKER_HEIGHT = SCREEN_SIZE[1] * 0.025

# The relative horizontal distance from the center of the screen
IMG_OFFSET = np.array([0.2, +0.025])
# The buttons resolution is roughly 1:1, but screen resolution is 1:1.77
ACTION_BUTTON_SIZE = EXPECTED_MONITOR_RESOLUTION * 0.07
# The relative horizontal and vertical distance from the center of the screen
ACTION_BUTTON_OFFSET = np.array([0.5375, 0.565])

# Don't modify these, as they are tailored to the instructions slides.
# Inst-accept button clickable-area relative size
INST_ACCEPT_BUTTON_SIZE = np.array([592 / 1280, 230 / 720])
# Inst-accept button clickable-area relative position
INST_ACCEPT_BUTTON_POS = [0, (-356 / 720) + INST_ACCEPT_BUTTON_SIZE[1] / 4]
INST_ACCEPT_TASK_DONE_BUTTON_POS = [0, (-313 / 720)
                                    + INST_ACCEPT_BUTTON_SIZE[1] / 4]

# Confirmation bar resolution is about 1:0.2045, but screen resolution is about 1:1.77
CONFIRM_BAR_SIZE = EXPECTED_MONITOR_RESOLUTION * np.array([1, 297 / 1413]) * 0.3
CONFIRM_BAR_POS = np.array([0, 0.5 - CONFIRM_BAR_SIZE[1] / 2])
# Don't modify these - they are tailored to the button size relative to the bar
CONFIRM_BAR_BUTTON_SIZE = np.array(
    [312 / 1413, 178 / 297]) * CONFIRM_BAR_SIZE * 0.75  # OMER
CONFIRM_BAR_BUTTON_POS = np.array([87.5 / 1413,
                                   0.5 - CONFIRM_BAR_SIZE[1]])

# Scale image resolution is about 1:2.52, but screen resolution is about 1:1.77
INTENSITY_SCALE_SIZE = EXPECTED_MONITOR_RESOLUTION * np.array(
    [1, 228 / 575]) * 0.25
INTENSITY_SCALE_POS = (([-0.5, 0.5])
                       + np.array([0.5, -0.5]) * INTENSITY_SCALE_SIZE)

# Mouse image resolution is about 1:1.06, but screen resolution is about 1:1.77
COLORS_MOUSE_KEY_SIZE = EXPECTED_MONITOR_RESOLUTION * np.array([1, 268 / 260]
                                                               ) * 0.15
COLORS_MOUSE_KEY_POS = np.array([0, 0.5 - COLORS_MOUSE_KEY_SIZE[1] / 2])

# Height of letters relative to the size of the window
TEXT_LABELS_SIZE = 0.025
