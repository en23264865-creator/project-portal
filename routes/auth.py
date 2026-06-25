from flask import Blueprint, request, jsonify
from models import db, bcrypt, User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

VALID_ROLES = ['Student', 'Guide', 'HoD', 'External Examiner']
VALID_DOMAINS = [
    'AI/ML', 'IoT', 'Cybersecurity', 'Web Development',
    'Data Science', 'Blockchain', 'Cloud Computing', 'Mobile Development'
]


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    required = ['name', 'email', 'password', 'role']
    for f in required:
        if not data.get(f):
            return jsonify({'message': f'{f} is required'}), 400

    role = data['role']
    if role not in VALID_ROLES:
        return jsonify({'message': 'Invalid role'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400

    # Guide must pick 2 or 3 domains
    domain1 = domain2 = domain3 = None
    if role == 'Guide':
        domains = data.get('domains', [])
        if len(domains) < 2 or len(domains) > 3:
            return jsonify({'message': 'Guide must select 2 or 3 domains'}), 400
        domain1 = domains[0]
        domain2 = domains[1]
        domain3 = domains[2] if len(domains) == 3 else None

    # External Examiner must pick sem + year
    exam_sem = exam_year = None
    if role == 'External Examiner':
        exam_sem  = data.get('exam_sem')
        exam_year = data.get('exam_year')
        if not exam_sem or not exam_year:
            return jsonify({'message': 'External Examiner must select sem and year'}), 400

    hashed = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user = User(
        name=data['name'],
        email=data['email'],
        password=hashed,
        role=role,
        domain1=domain1,
        domain2=domain2,
        domain3=domain3,
        exam_sem=exam_sem,
        exam_year=exam_year,
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Registered successfully', 'user': user.to_dict()}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    user = User.query.filter_by(email=data.get('email')).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if not bcrypt.check_password_hash(user.password, data.get('password', '')):
        return jsonify({'message': 'Invalid password'}), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({
        'token':   token,
        'user':    user.to_dict(),
    })


@auth_bp.route('/domains', methods=['GET'])
def get_domains():
    return jsonify({'domains': VALID_DOMAINS})
