from django.shortcuts import render

# Create your views here.
# monitoring/views.py
from django.http import StreamingHttpResponse
import cv2
import face_recognition as fr
import numpy as np
import os
import pygame
from time import sleep
import pyttsx3
from django.shortcuts import render


def index(request):
    return render(request, 'monitoring/index.html')


# Initialize face encoding data
faces = {}
encoded_faces = []
faces_name = []

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Function to play background music
def play_music(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(0.7)
    #pygame.mixer.music.play(-1)  # Loop the music

# Function to speak text
def speak_text(text,person):
    # Get available voices
    voices = engine.getProperty('voices')

    if person == "female":
        engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")
    else:
        engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0")
    # Set speech rate (optional)
    engine.setProperty('rate', 150)  # You can adjust the rate as needed

    # Set volume (optional)
    engine.setProperty('volume', 1)
    engine.say(text)
    engine.runAndWait()

def encode_faces():
    for dirpath, dnames, fnames in os.walk("./criminal_records"):
        for f in fnames:
            print(f)
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file(f"criminal_records/{f}")
                encoding = fr.face_encodings(face)
                if encoding:
                    faces[f.split(".")[0]] = encoding[0]
                else:
                    print(f"Warning: No face detected in {f}.")

    global encoded_faces, faces_name
    encoded_faces = list(faces.values())
    if not encoded_faces:
        print("No Faces were encoded. Ensure there is data in criminal_records folder.")
    faces_name = list(faces.keys())

def video_stream():
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        face_locations = fr.face_locations(frame)
        unknown_face_encodings = fr.face_encodings(frame, face_locations)
        for face_encoding in unknown_face_encodings:
            matches = fr.compare_faces(encoded_faces, face_encoding)
            name = "Regular Citizen"
            face_distances = fr.face_distance(encoded_faces, face_encoding)
            best_match_index = np.argmin(face_distances)
            print(face_distances[best_match_index])
            if face_distances[best_match_index] < 0.5:
                if matches[best_match_index]:
                    name = faces_name[best_match_index]

            if name != "Regular Citizen":
                play_music("beep-warning.mp3")
                speak_text(f"Known Offender named {name} came into the premises of our ATM, be vigilant!!!", "male")
                # Wait to let the music play a bit before exiting
                sleep(5)
                pygame.mixer.music.stop()

            # Overlay name
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

def video_feed(request):
    encode_faces()
    return StreamingHttpResponse(video_stream(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
