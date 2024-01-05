import os

from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("USERNAME_")
PASSWORD = os.getenv("PASSWORD_")
HOSTNAME = os.getenv("HOSTNAME_")
DATABASE = os.getenv("DATABASE_")
API_KEY = os.getenv("API_KEY")
DECRYPT_KEY = os.getenv("DECRYPT_KEY")

BROKER_URL = os.getenv("BROKER_URL")
MQTT_CLIENT_USERNAME = os.getenv("MQTT_CLIENT_USERNAME")
MQTT_CLIENT_PASSWORD = os.getenv("MQTT_CLIENT_PASSWORD")
