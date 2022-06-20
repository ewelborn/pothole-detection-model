# Primitive script for saving images from thermal camera

import cv2
import os

# Must have \ at the end
outputDirectory = "\\Datasets\\Thermal\\"
outputImage = "thermal{i}.png"
outputIndex = 0

cap = cv2.VideoCapture(1)

while (True):
    ret,frame = cap.read()
    cv2.imshow('frame',frame)

    inputKey = cv2.waitKey(1) & 0XFF
    if inputKey == ord('q') or inputKey == 27: # Esc
        break
    elif inputKey == ord(" "):
        # Check what image number we have to use
        while os.path.exists(outputDirectory+outputImage.format(i=outputIndex)):
            outputIndex += 1
        cv2.imwrite(outputDirectory+outputImage.format(i=outputIndex),frame)

cap.release()
cv2.destroyAllWindows()