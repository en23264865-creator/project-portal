import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ── Database ──────────────────────────────────────────────────
    _db_url = os.environ.get('DATABASE_URL', 'sqlite:///project_portal.db')
    # Render uses postgres:// — SQLAlchemy needs postgresql://
    if _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI      = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── JWT ───────────────────────────────────────────────────────
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'change_me_in_production_please')

    # ── Firebase ──────────────────────────────────────────────────
    # Set FIREBASE_CREDENTIALS env var to path of your serviceAccountKey.json
    # OR set FIREBASE_CREDENTIALS_JSON to the full JSON string (for Render)
    FIREBASE_CREDENTIALS      = os.environ.get('FIREBASE_CREDENTIALS', 'serviceAccountKey.json')
    FIREBASE_CREDENTIALS_JSON = os.environ.get('FIREBASE_CREDENTIALS_JSON', '')

    # ── Firebase client config (for frontend) ─────────────────────
    FIREBASE_API_KEY            = os.environ.get('FIREBASE_API_KEY', '')
    FIREBASE_AUTH_DOMAIN        = os.environ.get('FIREBASE_AUTH_DOMAIN', '')
    FIREBASE_PROJECT_ID         = os.environ.get('FIREBASE_PROJECT_ID', '')
    FIREBASE_STORAGE_BUCKET     = os.environ.get('FIREBASE_STORAGE_BUCKET', '')
    FIREBASE_MESSAGING_SENDER_ID= os.environ.get('FIREBASE_MESSAGING_SENDER_ID', '')
    FIREBASE_APP_ID             = os.environ.get('FIREBASE_APP_ID', '')
