import random
import cv2
from datetime import datetime
import numpy as np
import joblib
import easyocr
import pandas as pd
from pytube import YouTube
import time


def urltext(path):
    # print("Setting up camera...")
    yt = YouTube(path)
    stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
    cap = cv2.VideoCapture(stream.url)  # Use camera index 0 (default camera)
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
        # roi = frame[179:239,258:436]
        result = reader.readtext(frame, text_threshold=0.1)
                
        # Extract and concatenate the recognized text
        for res in result:
            recognized_text += res[1] + " "
        
        # Draw bounding boxes and display the recognized text
        conf_threshold = 0.1
        for y in result:
            if y[2] > conf_threshold:
                top_left_corner = [int(value) for value in y[0][0]]
                bottom_right_corner = [int(value) for value in y[0][2]]
                text_region = frame[top_left_corner[1]:bottom_right_corner[1], top_left_corner[0]:bottom_right_corner[0]]
                # color_label = detect_color(text_region)
                # Draw bounding box
                cv2.rectangle(frame, tuple(top_left_corner), tuple(bottom_right_corner), (0, 0, 255), 2)
                # Display the recognized text
                cv2.putText(frame, y[1], tuple(top_left_corner), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
                # Display the color label

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
    urltext()  # This is the combined code