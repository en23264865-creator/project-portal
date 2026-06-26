import re
from flask import Blueprint, request, jsonify, current_app
from models import db, bcrypt, User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

VALID_ROLES = ['Student', 'Guide', 'HoD', 'External Examiner']
VALID_DOMAINS = [
    'AI/ML', 'IoT', 'Cybersecurity', 'Web Development',
    'Data Science', 'Blockchain', 'Cloud Computing', 'Mobile Development',
]

# ═══════════════════════════════════════════════════════════════
# VALIDATION HELPERS
# ═══════════════════════════════════════════════════════════════

def validate_name(name):
    if not name or not name.strip():
        return 'Name is required'
    if len(name.strip()) < 2:
        return 'Name must be at least 2 characters'
    if not re.match(r'^[A-Za-z][A-Za-z\s\.]*$', name.strip()):
        return 'Name can only contain letters, spaces and dots — no numbers or special characters'
    return None

def validate_email(email):
    if not email or not email.strip():
        return 'Email is required'
    if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email.strip()):
        return 'Enter a valid email address (must contain @)'
    return None

def validate_password(password):
    if not password:
        return 'Password is required'
    if len(password) < 8:
        return 'Password must be at least 8 characters'
    if not re.search(r'[A-Z]', password):
        return 'Password must contain at least one uppercase letter (A-Z)'
    if not re.search(r'[a-z]', password):
        return 'Password must contain at least one lowercase letter (a-z)'
    if not re.search(r'\d', password):
        return 'Password must contain at least one number (0-9)'
    if not re.search(r'[!@#$%^&*()\-_=+\[\]{}|;:\'",.<>?/`~\\]', password):
        return 'Password must contain at least one special character (!@#$%^&* etc.)'
    return None

def validate_contact(contact):
    if not contact or not contact.strip():
        return None   # optional field
    digits = re.sub(r'\D', '', contact.strip())
    if len(digits) != 10:
        return 'Contact number must be exactly 10 digits'
    return None

# ═══════════════════════════════════════════════════════════════
# FIREBASE ADMIN — lazy init
# ═══════════════════════════════════════════════════════════════

_firebase_initialized = False

def init_firebase():
    global _firebase_initialized
    if _firebase_initialized:
        return True
    try:
        import firebase_admin
        from firebase_admin import credentials
        import json

        if firebase_admin._apps:
            _firebase_initialized = True
            return True

        cred_json = current_app.config.get('FIREBASE_CREDENTIALS_JSON', '')
        cred_file = current_app.config.get('FIREBASE_CREDENTIALS', 'serviceAccountKey.json')

        if cred_json:
            # JSON string stored in env var (recommended for Render)
            cred_dict = json.loads(cred_json)
            cred = credentials.Certificate(cred_dict)
        elif cred_file and __import__('os').path.exists(cred_file):
            cred = credentials.Certificate(cred_file)
        else:
            return False   # Firebase not configured — Google login unavailable

        firebase_admin.initialize_app(cred)
        _firebase_initialized = True
        return True
    except Exception as e:
        current_app.logger.warning(f'Firebase init failed: {e}')
        return False

# ═══════════════════════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════════════════════

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json or {}

        err = validate_name(data.get('name', ''))
        if err: return jsonify({'message': err}), 400

        err = validate_email(data.get('email', ''))
        if err: return jsonify({'message': err}), 400

        err = validate_password(data.get('password', ''))
        if err: return jsonify({'message': err}), 400

        err = validate_contact(data.get('contact', ''))
        if err: return jsonify({'message': err}), 400

        role = data.get('role', '')
        if role not in VALID_ROLES:
            return jsonify({'message': 'Please select a valid role'}), 400

        if User.query.filter_by(email=data['email'].strip().lower()).first():
            return jsonify({'message': 'This email is already registered'}), 400

        domain1 = domain2 = domain3 = None
        if role == 'Guide':
            domains = data.get('domains', [])
            if len(domains) < 2 or len(domains) > 3:
                return jsonify({'message': 'Guide must select 2 or 3 domains'}), 400
            domain1 = domains[0]
            domain2 = domains[1]
            domain3 = domains[2] if len(domains) == 3 else None

        exam_sem = exam_year = None
        if role == 'External Examiner':
            exam_sem  = data.get('exam_sem')
            exam_year = data.get('exam_year')
            if not exam_sem or not exam_year:
                return jsonify({'message': 'Please select semester and batch year'}), 400

        contact_digits = re.sub(r'\D', '', data.get('contact', '') or '')

        user = User(
            name      = data['name'].strip(),
            email     = data['email'].strip().lower(),
            password  = bcrypt.generate_password_hash(data['password']).decode('utf-8'),
            role      = role,
            contact   = contact_digits if contact_digits else None,
            domain1   = domain1,
            domain2   = domain2,
            domain3   = domain3,
            exam_sem  = int(exam_sem)  if exam_sem  else None,
            exam_year = int(exam_year) if exam_year else None,
        )
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=str(user.id))
        return jsonify({
            'message': 'Account created successfully!',
            'token':   token,
            'user':    user.to_dict(),
        }), 201

    except Exception as e:
        db.session.rollback()
        import traceback
        current_app.logger.error(f'Register error: {e}\n{traceback.format_exc()}')
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json or {}

        email    = data.get('email', '').strip().lower()
        password = data.get('password', '')

        if not email:
            return jsonify({'message': 'Email is required'}), 400
        if not password:
            return jsonify({'message': 'Password is required'}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'message': 'No account found with this email address'}), 404

        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({'message': 'Incorrect password. Please check and try again.'}), 401

        token = create_access_token(identity=str(user.id))
        return jsonify({'token': token, 'user': user.to_dict()})

    except Exception as e:
        import traceback
        current_app.logger.error(f'Login error: {e}\n{traceback.format_exc()}')
        return jsonify({'message': f'Login failed: {str(e)}'}), 500


@auth_bp.route('/google', methods=['POST'])
def google_login():
    """
    Receive Firebase ID token from frontend after Google Sign-In.
    Verify it server-side, then issue our own JWT.
    """
    data     = request.json or {}
    id_token = data.get('id_token', '')
    if not id_token:
        return jsonify({'message': 'Firebase ID token is required'}), 400

    if not init_firebase():
        return jsonify({'message': 'Google Sign-In is not configured on this server'}), 503

    try:
        from firebase_admin import auth as fb_auth
        decoded      = fb_auth.verify_id_token(id_token)
        firebase_uid = decoded.get('uid')
        email        = decoded.get('email', '').lower()
        name         = decoded.get('name', email.split('@')[0].replace('.', ' ').title())
    except Exception as e:
        return jsonify({'message': f'Google verification failed: {str(e)}'}), 401

    # Find existing user
    user = (
        User.query.filter_by(firebase_uid=firebase_uid).first() or
        User.query.filter_by(email=email).first()
    )

    if user:
        if not user.firebase_uid:
            user.firebase_uid = firebase_uid
            db.session.commit()
    else:
        # New user via Google — ask for role in the request
        role = data.get('role', 'Student')
        if role not in VALID_ROLES:
            role = 'Student'
        user = User(
            name         = name,
            email        = email,
            password     = bcrypt.generate_password_hash(firebase_uid + 'google').decode('utf-8'),
            role         = role,
            firebase_uid = firebase_uid,
        )
        db.session.add(user)
        db.session.commit()

    token = create_access_token(identity=str(user.id))
    return jsonify({'token': token, 'user': user.to_dict()})


@auth_bp.route('/firebase-config', methods=['GET'])
def firebase_config():
    """Return Firebase client config to the frontend."""
    cfg = current_app.config
    return jsonify({
        'apiKey':            cfg.get('FIREBASE_API_KEY', ''),
        'authDomain':        cfg.get('FIREBASE_AUTH_DOMAIN', ''),
        'projectId':         cfg.get('FIREBASE_PROJECT_ID', ''),
        'storageBucket':     cfg.get('FIREBASE_STORAGE_BUCKET', ''),
        'messagingSenderId': cfg.get('FIREBASE_MESSAGING_SENDER_ID', ''),
        'appId':             cfg.get('FIREBASE_APP_ID', ''),
    })


@auth_bp.route('/domains', methods=['GET'])
def get_domains():
    return jsonify({'domains': VALID_DOMAINS})
