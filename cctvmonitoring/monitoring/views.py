from django.shortcuts import render

# Create your views here.
# monitoring/views.py
from django.http import StreamingHttpResponse
import cv2
import face_recognition as fr
import numpy as np
import os
import pygame
import time
import pyttsx3
from django.shortcuts import render

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import base64
import cv2
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

import threading

def index(request):
    return render(request, 'monitoring/index.html')

# Initialize face encoding data
faces = {}
encoded_faces = []
faces_name = []

# Initialize pyttsx3 engine
dic = {}

@csrf_exempt  # Disable CSRF for simplicity (enable CSRF in production)
def process_frame(request):
    if request.method == "POST":
        try:
            # Get the frame from the request
            data = json.loads(request.body)
            frame_data = data.get("frame")

            if not frame_data:
                return JsonResponse({"error": "No frame data received"}, status=400)

            # Decode the Base64-encoded frame
            frame_data = base64.b64decode(frame_data.split(",")[1])
            np_frame = np.frombuffer(frame_data, np.uint8)
            frame = cv2.imdecode(np_frame, cv2.IMREAD_COLOR)

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
                    if name in dic and int(time.time()) - int(dic[name]) < 60:
                        print("Current Time" + str(time.time()) + "Previous Time" + str(dic[name]))
                    else:
                        current_unix_time = int(time.time())
                        dic[name] = current_unix_time
                        play_music_in_thread("beep-warning.mp3")
                        mail(name)
                        speak_in_thread(
                            f"Known Offender named {name} came into the premises of our ATM, be vigilant!!!", "male")
                        # Wait to let the music play a bit before exiting


            return JsonResponse({"status": "Frame processed successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)


def play_music_in_thread(file):
    t = threading.Thread(target=play_music, args=(file,))
    t.start()

# Function to play background music
def play_music(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)  # Loop the music
    time.sleep(5)
    pygame.mixer.music.stop()

def mail(name):
    # Email details
    sender_email = "chandanamvamsik@gmail.com"
    app_password = "fobrxlzhrllpklgc"  # Use the generated app password
    recipient_email = "krishnavamsi1225@gmail.com"
    subject = "Alert!! Known Offender entered ATM premises"
    body = f"Known Offender {name} enterred ATM premises. Be vigilant!!"

    # Create the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # SMTP server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Start TLS encryption
        server.login(sender_email, app_password)  # Authenticate with the app password

        # Send the email
        server.sendmail(sender_email, recipient_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()

def speak_in_thread(text,person):
    t = threading.Thread(target=speak_text, args=(text,person))
    t.start()

# Function to speak text
def speak_text(text,person):
    # Get available voices
    engine = pyttsx3.init()
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
    for dirpath, dnames, fnames in os.walk("criminal_records"):
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