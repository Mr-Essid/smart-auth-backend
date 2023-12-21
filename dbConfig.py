import os

from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("USERNAME_")
PASSWORD = os.getenv("PASSWORD_")
HOSTNAME = os.getenv("HOSTNAME_")
DATABASE = os.getenv("DATABASE_")
