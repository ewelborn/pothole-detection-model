# Script for cleaning up datasets for use in YOLO training
# Includes the following features:
#   - Automatically renaming files to fit into an existing dataset
#       + ex. pothole-1.jpg, pothole-2.jpg, etc. --> data1023.png, data1024.png, etc.
#       + supports conversion between different file extensions (via opencv)
#   - Converting XML formatted bounding boxes to YOLO formatted bounding boxes

import os
import cv2
from xml.etree import ElementTree as ET

# Where are all of the images stored?
folderPath = "\\Datasets\\Potholes\\testing ground\\"

fileNameScheme = "img-{i}"
fileExtension = ".jpg"
fileIndices = (1,665) # Inclusive

# If you want to rename files <=============
RENAME_FILE = True

# The original file will be destroyed (or directly renamed) if this is true. If you
# do not have a backup of the original dataset, then keep this set to false!
destroyOriginalFiles = True

targetFileNameScheme = "potholes{i}"
targetFileExtension = ".png"

# Where will our images go? The images will be renamed with the following index,
# increasing by 1 per image.
# Ex. if fileIndices = (744,746) and targetFileIndex = 100, then
#     a744, a745, a746 --> b100, b101, b102
targetFileIndex = 696

# If you want to export XML formatted bounding boxes as YOLO bounding boxes <=============
# DOES NOT WORK WITH MULTICLASS IMAGES
EXPORT_XML_AS_YOLO = True

# The original XML file will be destroyed  if this is true. If you
# do not have a backup of the original XML file, then keep this set to false!
destroyOriginalXMLFiles = True

# !!!
# End of configuration
# !!!

if folderPath[-1] != "\\":
    folderPath = folderPath + "\\"

for i in range(fileIndices[0],fileIndices[1] + 1):
    fileName = fileNameScheme.format(i=i)
    
    if RENAME_FILE:
        offset = i - fileIndices[0] + targetFileIndex
        oldFilePath = folderPath+fileName+fileExtension
        newFilePath = folderPath+targetFileNameScheme.format(i=offset)+targetFileExtension

        if fileExtension == targetFileExtension:
            # No conversion necessary
            if destroyOriginalFiles:
                os.rename(oldFilePath, newFilePath)
            else:
                # Must copy the files instead
                image = cv2.imread(oldFilePath)
                cv2.imwrite(newFilePath,image)
        else:
            # Must convert using opencv
            image = cv2.imread(oldFilePath)
            cv2.imwrite(newFilePath,image)
            if destroyOriginalFiles:
                os.remove(oldFilePath)

    if EXPORT_XML_AS_YOLO:
        offset = i - fileIndices[0] + targetFileIndex
        oldFilePath = folderPath+fileName+".xml"
        newFilePath = folderPath+targetFileNameScheme.format(i=offset)+".txt"

        # https://stackoverflow.com/questions/3217487/how-to-get-all-the-info-in-xml-into-dictionary-with-python
        xml = ET.parse(oldFilePath)
        
        imageWidth = int(xml.find("size").find("width").text)
        imageHeight = int(xml.find("size").find("height").text)

        newFileText = ""

        for obj in xml.findall("object"):
            bndbox = obj.find("bndbox")
            xMin = int(bndbox.find("xmin").text)
            yMin = int(bndbox.find("ymin").text)
            xMax = int(bndbox.find("xmax").text)
            yMax = int(bndbox.find("ymax").text)
            
            centerX = ((xMax + xMin) / 2) / imageWidth
            centerY = ((yMax + yMin) / 2) / imageHeight
            width = (xMax - xMin) / imageWidth
            height = (yMax - yMin) / imageHeight
            
            newFileText += "0 {0:.5f} {1:.5f} {2:.5f} {3:.5f}\n".format(centerX,centerY,width,height)

        newFile = open(newFilePath,"w")
        newFile.write(newFileText)
        newFile.close()

        if destroyOriginalXMLFiles:
            os.remove(oldFilePath)