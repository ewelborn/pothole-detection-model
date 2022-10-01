import numpy as np
import cv2
import copy
import os

### IMPORT AND VALIDATE CONFIG SETTINGS

import config

# Make sure the detection model is valid
config.DETECTION_MODEL = config.DETECTION_MODEL.upper()
if not(config.DETECTION_MODEL in ["YOLO"]):
    print(config.DETECTION_MODEL, "is not a valid detection model")
    print("Please try \"YOLO\"")
    exit()

# Make sure the image exists
if not os.path.isfile(config.INPUT_PATH):
    print("File at INPUT_PATH does not exist:", str(config.INPUT_PATH))
    exit()

# Make sure the output image does *not* exist (if applicable)
if config.SAVE_RESULT and config.OVERWRITE_PREVIOUS_RESULT == False:
    if os.path.isfile(config.OUTPUT_PATH):
        print("Output image already exists at the following path:", str(config.OUTPUT_PATH))
        exit()

### START PROCESSING

inputImage = cv2.imread(config.INPUT_PATH)
inputImageHeight = inputImage.shape[0]
inputImageWidth = inputImage.shape[1]

outputImage = copy.deepcopy(inputImage)

imageBlob = cv2.dnn.blobFromImage(inputImage, 0.003922, (416, 416), swapRB=True, crop=False)

class_labels = ["pothole"]
class_colors = [(255,0,0)]

yolo_model = cv2.dnn.readNetFromDarknet(config.YOLO_CONFIG_PATH, config.YOLO_WEIGHTS_PATH)
yolo_layers = yolo_model.getLayerNames()
yolo_output_layer = [yolo_layers[yolo_layer-1] for yolo_layer in yolo_model.getUnconnectedOutLayers()]

yolo_model.setInput(imageBlob)
object_detection_layers = yolo_model.forward(yolo_output_layer)

class_ids_list = []
boxes_list = []
confidences_list = []

for object_detection_layer in object_detection_layers:
    for object_detection in object_detection_layer:
        all_scores = object_detection[5:]
        predicted_class_id = np.argmax(all_scores)
        prediction_confidence = all_scores[predicted_class_id]

        if prediction_confidence > 0.2:
            predicted_class_label = class_labels[predicted_class_id]

            bounding_box = object_detection[0:4] * np.array([inputImageWidth, inputImageHeight, inputImageWidth, inputImageHeight])
            (box_center_x_point, box_center_y_point, box_width, box_height) = bounding_box.astype("int")
            start_x_point = int(box_center_x_point - (box_width / 2))
            start_y_point = int(box_center_y_point - (box_height / 2))

            class_ids_list.append(predicted_class_id)
            confidences_list.append(float(prediction_confidence))
            boxes_list.append([start_x_point,start_y_point,int(box_width),int(box_height)])

max_value_ids = cv2.dnn.NMSBoxes(boxes_list,confidences_list,0.5,0.4)
for max_value_id in max_value_ids:
    max_class_id = max_value_id
    box = boxes_list[max_class_id]
    start_x_point = box[0]
    start_y_point = box[1]
    box_width = box[2]
    box_height = box[3]

    predicted_class_id = class_ids_list[max_class_id]
    predicted_class_label = class_labels[predicted_class_id]
    prediction_confidence = confidences_list[max_class_id]

    end_x_point = start_x_point + box_width
    end_y_point = start_y_point + box_height

    box_color = class_colors[predicted_class_id]
    box_color = [int(c) for c in box_color]

    predicted_class_label = "{}: {:.2f}%".format(predicted_class_label, prediction_confidence * 100)
    print("predicted object {}".format(predicted_class_label))

    cv2.rectangle(outputImage, (start_x_point,start_y_point), (end_x_point,end_y_point), box_color, config.DRAWING_THICKNESS)
    cv2.putText(outputImage, predicted_class_label, (start_x_point,start_y_point - 10), cv2.FONT_HERSHEY_SIMPLEX, config.TEXT_SCALING, box_color, config.TEXT_THICKNESS)

if config.SAVE_RESULT:
    cv2.imwrite(config.OUTPUT_PATH, outputImage)

if config.TERMINAL_ONLY == False:
    cv2.imshow("Detection Output", outputImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
