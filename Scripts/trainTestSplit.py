# Script for generating training and testing files for YOLO
import numpy as np
from sklearn.model_selection import train_test_split

filePathTemplate = "pothole_data/pothole_images/potholes{i}.png"

fileIndices = (1,1360) # Inclusive

testPercentage = 0.3 # The rest will be given to training

outputPath = "\\Datasets\\Potholes\\"

### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
### End of config
### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

if outputPath[-1] != "\\":
    outputPath = outputPath + "\\"

filePaths = [filePathTemplate.format(i=i) for i in range(fileIndices[0],fileIndices[1]+1)]

train,test = train_test_split(filePaths,test_size=testPercentage)

trainFile = open(outputPath+"training.txt","w")
trainFile.write("\n".join(train))
trainFile.close()

testFile = open(outputPath+"testing.txt","w")
testFile.write("\n".join(test))
testFile.close()