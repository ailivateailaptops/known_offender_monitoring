# Known Offender Monitoring Server

This project is a server-side application designed for monitoring known offenders using CCTV systems. It includes functionalities like accessing and managing criminal records, triggering warnings, and providing an endpoint for monitoring activities.

## Project Structure

The main components of the project are:
- **`manage.py`**: The main entry point for managing the application.
- **`monitoring/`**: The primary endpoint for monitoring activities.
- **`criminal_records/`**: Stores records of known offenders.
- **`cctvmonitoring/`**: Contains the core application logic.
- **Database**: A SQLite3 database (`db.sqlite3`) for storing offender data.

## Requirements

Create requirements.txt file and add the following libraries to your requirements.txt file:

```
face_recognition
numpy
opencv-python
pyttsx3
pygame
Pillow
```

The application requires the following Python packages to run:

- Django
- djangorestframework
- sqlite3 (built-in with Python)

Ensure you have these packages installed. To create a `requirements.txt` file, run:

```bash
pip install -r requirements.txt
```

This will list all the installed packages in your environment.

## Installation

1. Clone or download the project to your local machine.

   ```bash
   git clone <repository_url>
   cd known_offender_monitoring-serverside
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
   python manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000/monitoring/`.

## Usage

- Use the **`monitoring/`** endpoint to interact with the application.
- Ensure **`criminal_records`** folder contains the relevant offender data for the monitoring to function effectively.

## Additional Resources

- Audio warnings such as `beep-warning.mp3` and `welcome.mp3` are included for alert notifications.

## Notes

- Ensure proper setup and configuration of the database before running the server.
- If additional packages are needed, install them and update the `requirements.txt` file accordingly.

---
