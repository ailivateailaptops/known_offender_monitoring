from time import sleep

import face_recognition as fr
import numpy as np
import os
import cv2
import tkinter as tk
from tkinter import PhotoImage
import pyttsx3
import pygame

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Function to play background music
def play_music(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)  # Loop the music

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
    encoded_data = {}
    for dirpath, dnames, fnames in os.walk("./criminal_records"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file(f"criminal_records/{f}")
                encoding = fr.face_encodings(face)
                if encoding:
                    encoded_data[f.split(".")[0]] = encoding[0]
                else:
                    print(f"Warning: No face detected in criminal photo {f}. Skipping...")
    return encoded_data

def process_frame(frame, encoded_faces, faces_name):
    # Initialize text-to-speech engine

    # Detect faces in the frame
    face_locations = fr.face_locations(frame)
    unknown_face_encodings = fr.face_encodings(frame, face_locations)
    face_names = []

    for face_encoding in unknown_face_encodings:
        matches = fr.compare_faces(encoded_faces, face_encoding)
        name = "Regular Citizen"
        face_distances = fr.face_distance(encoded_faces, face_encoding)
        best_match_index = np.argmin(face_distances)
        least_value = face_distances[best_match_index]
        if least_value < 0.4:
            if matches[best_match_index]:
                name = faces_name[best_match_index]

        # Provide audio feedback when a face is identified
        face_names.append(name)
        if name != "Regular Citizen":
            play_music("beep-warning.mp3")
            speak_text(f"Known Offender named {name} came into the premises of our ATM, be vigilant!!!","male")
            # Wait to let the music play a bit before exiting
            sleep(5)
            pygame.mixer.music.stop()
            break
    return face_locations, face_names

def handle_real_time():
    # Initialize text-to-speech engine
    play_music("welcome.mp3")
    sleep(5)
    speak_text(
        f"Welcome to Elevate AI Trainings.. experience the future .. Starting CCTV Monitoring System for Known Offenders!!!","female")
    sleep(15)
    pygame.mixer.music.stop()

    faces = encode_faces()
    encoded_faces = list(faces.values())
    faces_name = list(faces.keys())
    video_frame = True
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame.")
            break
        if video_frame:
            face_locations, face_names = process_frame(frame, encoded_faces, faces_name)
        video_frame = not video_frame
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            cv2.rectangle(frame, (left - 20, top - 20), (right + 20, bottom + 20), (0, 255, 0), 2)
            cv2.rectangle(frame, (left - 20, bottom - 15), (right + 20, bottom + 20), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left - 20, bottom + 15), font, 0.85, (255, 255, 255), 2)
        cv2.imshow('CCTV Monitoring System for Known Offenders', frame)
        key_pressed = cv2.waitKey(1)  # Gets the key pressed
        if key_pressed & 0xFF == ord('q'):  # Checks if 'q' is pressed
            print("Q key detected! Breaking the loop...")
            break
    video_capture.release()
    cv2.destroyAllWindows()

root = tk.Tk()
root.title("CCTV Monitoring System for Known Offenders")
root.geometry("1024x760")

background_image = PhotoImage(file="background.png")
# Create a Label widget to display the image
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)  # Set it to fill the window

title_label = tk.Label(root, text="Ailivate AI Trainings CCTV Monitoring System ", font=("Helvetica", 16))
title_label.pack(pady=10)
real_time_btn = tk.Button(root, text="Start Offender Monitoring", command=handle_real_time,font=("Arial", 20, "bold"),fg="black",bg="lightblue",height=3,width=30)
real_time_btn.pack(pady=10)
root.mainloop()