# CCTV Monitoring System for Known Offenders

This repository contains a Python-based CCTV Monitoring System designed to identify known offenders using facial recognition. It integrates various features like real-time face detection, text-to-speech alerts, email notifications, and GUI-based interaction.

---

## Features

- **Facial Recognition**: Uses the `face_recognition` library to identify individuals.
- **Real-Time Monitoring**: Captures live video feed from a camera.
- **Alert System**: Sends email notifications and plays warning sounds if a known offender is detected.
- **Text-to-Speech**: Provides audio alerts using `pyttsx3`.
- **Graphical User Interface**: Interactive GUI using `Tkinter`.

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/cctv-monitoring-system.git
   cd cctv-monitoring-system
   ```

2. **Install Dependencies**
   Ensure you have Python 3.x installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

   Create `requirements.txt` file and add the following libraries to your `requirements.txt` file:

   ```
   face_recognition
   numpy
   opencv-python
   pyttsx3
   pygame
   Pillow
   ```

3. **Prepare Criminal Records**

   - Create a folder named `criminal_records` in the project directory.
   - Add images of known offenders (JPEG or PNG format).

4. **Update Email Credentials**

   - Replace the `sender_email` and `app_password` variables in `driver.py` with your credentials.
   - Generate an app password for secure email sending.

5. **Run the Application**
   Execute the script:

   ```bash
   python driver.py
   ```

---

## Usage

1. Launch the application.
2. Click the **Start Offender Monitoring** button to begin real-time monitoring.
3. The system will:
   - Detect faces and compare them with the `criminal_records` database.
   - Alert via text-to-speech and warning sounds if a match is found.
   - Send an email notification with the offender’s name.

---

## File Structure

```
.
|-- criminal_records/       # Directory for offender images
|-- driver.py               # Main script
|-- background.png          # Background image for GUI
|-- beep-warning.mp3        # Audio file for alerts
|-- welcome.mp3             # Welcome message audio file
|-- requirements.txt        # Python dependencies
```

---

## Dependencies

- Python 3.x
- `face_recognition`
- `numpy`
- `opencv-python`
- `pyttsx3`
- `pygame`
- `Pillow`

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Libraries Used**:
  - [face_recognition](https://github.com/ageitgey/face_recognition)
  - [OpenCV](https://opencv.org/)
- Inspiration: [Ailivate AI Trainings](https://ailivate.ai)
