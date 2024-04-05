import random
import cv2
from datetime import datetime
import numpy as np
from ultralytics import YOLO
import joblib
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

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

def ip_obj(path):
    # print("Setting up camera...")
    cap = cv2.VideoCapture(0)
    add = path  # Use camera index 0 (default camera)
    cap.open(add)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    print("Loading model...")


    while True:
        ret, frame = cap.read()  # Read a frame from the camera

        if not ret:
            print("Error: Failed to capture frame")
            break

        detect_params = model.predict(source=[frame], conf=0.45, save=False)

        DP = detect_params[0].numpy()
        print(DP)
        
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
    ip_obj()  # This is the combined code