# importing libraries
import random
import cv2
from datetime import datetime
import numpy as np
from ultralytics import YOLO
import joblib
import easyocr
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from pytube import *

# load color detection model
color_detection_model = joblib.load("Colour Detection\\color_detection_model.pkl")

# code for object :
my_file = open("Colour Detection\\coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")
my_file.close()

detection_colors = []
for i in range(len(class_list)):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    detection_colors.append((b, g, r))

model = YOLO("Colour Detection\\yolov8m.pt", "v8")

frame_wid = 640
frame_hyt = 480

# code for text: 
def detect_color(text_region):
    # Check if the text region is not empty
    if text_region is not None:
        # Convert text region to RGB
        rgb_text_region = cv2.cvtColor(text_region, cv2.COLOR_BGR2RGB)
        # Calculate the average RGB values
        avg_color = np.mean(rgb_text_region, axis=(0, 1)).astype(int)
        # Predict the color label for the average RGB values
        color_label = color_detection_model.predict([avg_color])[0]
        return color_label
    else:
        return "Unknown"
    
'''
# function to get the co-ordinates of ROI
def POINTS(event, x,y, flags, param):
    if event==cv2.EVENT_MOUSEMOVE:
        colorsBGR=[x,y]
        print(colorsBGR)

cv2.namedWindow('ROI')
cv2.setMouseCallback('ROI', POINTS)
'''
    
def ip_col(path):
    # OpenCV video capture
    cap = cv2.VideoCapture(0)
    cap.open(path)
    # print("Setting up camera...")
    # cap = cv2.VideoCapture(path)  # Use camera index 0 (default camera)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    print("Loading model...")
    reader = easyocr.Reader(["en"])

    # Initialize variables to store the recognized text and corresponding timestamps
    recognized_text = ""
    last_update_time = datetime.now()

    while True:
        ret, frame = cap.read()  # Read a frame from the camera

        if not ret:
            print("Error: Failed to capture frame")
            break

        # Get current time
        current_time = datetime.now()
        roi = frame[179:239,258:436]
        detect_params = model.predict(source=[frame], conf=0.45, save=False)

        DP = detect_params[0].numpy()
        print(DP)
        result = reader.readtext(roi, text_threshold=0.1)
        
        if len(DP) != 0:
            for i in range(len(detect_params[0])):
                print(i)

                boxes = detect_params[0].boxes
                box = boxes[i]
                clsID = box.cls.numpy()[0]
                conf = box.conf.numpy()[0]
                bb = box.xyxy.numpy()[0]
                cv2.rectangle(
                    frame,
                    (int(bb[0]), int(bb[1])),
                    (int(bb[2]), int(bb[3])),
                    detection_colors[int(clsID)],
                    3,
                )
                # font = cv2.FONT_HERSHEY_COMPLEX
                font = cv2.FONT_HERSHEY_PLAIN
                cv2.putText(
                    frame,
                    class_list[int(clsID)] + " " + str(round(conf, 3)) + "%",
                    (int(bb[0]), int(bb[1]) - 10),
                    font,
                    1,
                    (255, 255, 255),
                    2,
                )
                # Extract RGB values of the detected object
                object_img = roi[int(bb[1]):int(bb[3]), int(bb[0]):int(bb[2])]
                avg_color = np.mean(object_img, axis=(0, 1)).astype(int)
                rgb_color = avg_color[::-1]  # OpenCV uses BGR, we need RGB
                color_label = color_detection_model.predict([rgb_color])[0]
                
                # Convert color_label to a string before concatenating
                color_label_str = str(color_label)

                cv2.putText(
                    frame,
                    "Color: " + color_label_str,  # Concatenate with the color_label_str
                    (int(bb[0]), int(bb[1]) - 30),
                    font,
                    1,
                    (0, 255, 0),
                    2,
                )
                
        # Extract and concatenate the recognized text
        for res in result:
            recognized_text += res[1] + " "

        # Check if enough time has passed since the last update
        if (current_time - last_update_time).total_seconds() > 2:  # Adjust the delay time as needed
            # Print the recognized text, color, and reset variables
            if recognized_text:
                color_label = detect_color(roi)
                print(f"Text: {recognized_text.strip()}, Color: {color_label}, Timestamp: {current_time.strftime('%H:%M:%S')}")
                recognized_text = ""
            last_update_time = current_time
        
        # Draw bounding boxes and display the recognized text
        conf_threshold = 0.1
        for y in result:
            if y[2] > conf_threshold:
                top_left_corner = [int(value) for value in y[0][0]]
                bottom_right_corner = [int(value) for value in y[0][2]]
                text_region = roi[top_left_corner[1]:bottom_right_corner[1], top_left_corner[0]:bottom_right_corner[0]]
                color_label = detect_color(text_region)
                # Draw bounding box
                cv2.rectangle(roi, tuple(top_left_corner), tuple(bottom_right_corner), (0, 0, 255), 2)
                # Display the recognized text
                cv2.putText(roi, y[1], tuple(top_left_corner), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
                # Display the color label
                cv2.putText(roi, f'Color: {color_label}', (top_left_corner[0], top_left_corner[1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

        yield frame

        # Display the frame
        # cv2.imshow("Frame", frame)

        # Check for keyboard input to quit
        # if cv2.waitKey(1) & 0xFF == ord("q"):
            # break

    # Release the camera
    # cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    ip_col()  # This is the combined code