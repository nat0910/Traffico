import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now you can use os.getenv to access the environment variables
SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///data/mydatabase.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False


HELMET_MODEL_PATH = "yolo_models/helmet/helmet-detection-weights.pt"
SPEED_MODEL_PATH = "yolo_models/speed-detection/speed-detection-weights.pt"
SEATBELT_MODEL_PATH = "yolo_models/seatbealt/seatbealt-detection-weights.pt"
LICENSE_PLATE_MODEL_PATH ="yolo_models/license-plate/license-plate-weights.pt"

# SIGNAL_MODEL_PATH = ""