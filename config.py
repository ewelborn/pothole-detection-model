# If true, then no windows will be drawn to the screen - all progress will be shared
# through the terminal window only.
# NOTE: This setting is meant for rendering videos in the background where progress
#       being displayed in real-time is not necessary. This setting is especially
#       useful on terminal-only environments where OpenCV may not be able to open
#       any windows.
TERMINAL_ONLY = True

# Image file to read
# NOTE: In the future, this script will support video files
INPUT_PATH = "C:\\Users\\saldo\\OneDrive - tarleton.edu (NTNET)\\Research\\Misc Drone Data\\9-26\\org_d5879a5faa0cf871ba36fa4e30dfdad6_raw.jpg"

# Do you want the results stored to your computer as a new image? 
# Is overwriting a previous output image okay?
SAVE_RESULT = True
OVERWRITE_PREVIOUS_RESULT = False

# Image to write to
# NOTE: This has no effect if SAVE_RESULT = False
OUTPUT_PATH = "potholes6.png"

# What detection model are we using? (As of now, only YOLO)
DETECTION_MODEL = "YOLO"

# Where are the YOLOv4 configuration and weight files contained? (No effect if DETECTION_MODEL != "YOLO")
YOLO_CONFIG_PATH = "pothole_yolov4.cfg"
YOLO_WEIGHTS_PATH = "pothole_yolov4_best.weights"

# How thick should the drawing be on the output image?
DRAWING_THICKNESS = 5

# How large and thick should the text be on the output image?
TEXT_SCALING = 1.5
TEXT_THICKNESS = 2