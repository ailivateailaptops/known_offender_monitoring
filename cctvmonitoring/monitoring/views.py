
import cv2
import numpy as np
import pyttsx3
import pygame
from django.http import StreamingHttpResponse
from django.shortcuts import render
from ultralytics import YOLO

# Initialize text-to-speech engine
engine = pyttsx3.init()
pygame.mixer.init()


def play_alarm():
    pygame.mixer.music.load("alarm.mp3")  # Add an alarm sound file in the project directory
    pygame.mixer.music.play()


def speak(text):
    engine.say(text)
    engine.runAndWait()


# Load YOLO model (you can use a custom-trained model if needed)
model = YOLO("yolov8n.pt")

# Define harmful objects
harmful_objects = ["knife", "gun", "scissors"]


def detect_objects():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLO detection
        results = model(frame)
        for result in results:
            for obj in result.boxes.data:
                x1, y1, x2, y2, conf, cls = obj.tolist()
                label = model.names[int(cls)]

                # Check if the detected object is harmful
                if label in harmful_objects:
                    play_alarm()
                    speak(f"Warning! {label} detected!")

                    # Draw bounding box and label
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                    cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Encode frame to JPEG
        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
    cap.release()


def video_feed(request):
    return StreamingHttpResponse(detect_objects(), content_type='multipart/x-mixed-replace; boundary=frame')


def index(request):
    return render(request, 'index.html')
