import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'db' / 'store.db'
DEBUG = True
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
