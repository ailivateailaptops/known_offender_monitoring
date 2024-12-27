# Known Offender Monitoring Client

This project is a client-side application designed to interact with a server-side system for monitoring known offenders using CCTV systems. It includes functionalities for managing offender records, playing warning sounds, and communicating with the server through the **`monitoring/`** endpoint.

## Project Structure

The main components of the project are:
- **`manage.py`**: The main entry point for managing the client application.
- **`middleware.py`**: Handles client-side middleware functionalities.
- **`monitoring/`**: The primary endpoint for client-server interactions.
- **`criminal_records/`**: Stores local offender records.
- **`cctvmonitoring/`**: Contains core client application logic.
- **Database**: A SQLite3 database (`db.sqlite3`) for storing offender data.

## Requirements

The application requires the following Python packages to run:
Create requirements.txt file and add the following libraries to your requirements.txt file:

```
face_recognition
numpy
opencv-python
pyttsx3
pygame
Pillow
django_extensions
pyopenssl
```

Ensure you have these packages installed. To create a `requirements.txt` file, run:

```bash
pip freeze > requirements.txt
```

This will list all the installed packages in your environment.

## Installation

1. Clone or download the project to your local machine.

   ```bash
   git clone <repository_url>
   cd known_offender_monitoring-clientside
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies (once `requirements.txt` is created):

   ```bash
   pip install -r requirements.txt
   ```

4. Migrate the database:

   ```bash
   python manage.py migrate
   ```

5. Run the development server:

   ```bash
   python manage.py runserver_plus --cert-file cert.pem --key-file key.pem IP_ADDRESS:8080
   ```

6. Access the client application at `https://IP_ADDRESS:8000/monitoring/`.

## Usage

- Follow any standard guide for creation of cert.pem and key.pem files

## Usage

- The **`monitoring/`** endpoint communicates with the server to fetch and display offender data.
- Ensure the server-side application is running and properly configured for seamless operation.

## Additional Resources

- Audio warnings such as `beep-warning.mp3` and `welcome.mp3` are included for alert notifications.

## Notes

- Ensure proper setup and configuration of the database before running the client.
- If additional packages are needed, install them and update the `requirements.txt` file accordingly.
