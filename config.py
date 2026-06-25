import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # PostgreSQL Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:password@localhost:5432/project_portal'
    )
    # Render PostgreSQL URIs sometimes use postgres:// — fix it
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super_secret_jwt_key_change_in_prod')

    # Firebase Admin SDK — path to serviceAccountKey.json
    FIREBASE_CREDENTIALS = os.environ.get('FIREBASE_CREDENTIALS', 'serviceAccountKey.json')

    # Upload folder
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
