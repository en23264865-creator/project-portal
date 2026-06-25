from flask import Blueprint, request, jsonify
from models import db, User, Project
from flask_jwt_extended import jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__)


@users_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    data = user.to_dict()

    if user.role == 'Guide':
        students = db.session.query(User).join(
            Project, Project.student_id == User.id
        ).filter(Project.guide_id == user_id).distinct().all()
        data['students'] = [s.to_dict() for s in students]
        data['projects'] = [p.to_dict() for p in Project.query.filter_by(guide_id=user_id).all()]

    elif user.role == 'External Examiner':
        projects = Project.query.filter_by(
            sem=user.exam_sem, year=user.exam_year
        ).all()
        data['projects'] = [p.to_dict() for p in projects]

    elif user.role == 'HoD':
        data['projects'] = [p.to_dict() for p in Project.query.all()]

    elif user.role == 'Student':
        data['projects'] = [p.to_dict() for p in Project.query.filter_by(student_id=user_id).all()]

    return jsonify(data)


@users_bp.route('/guides', methods=['GET'])
def get_guides():
    guides = User.query.filter_by(role='Guide').all()
    return jsonify([g.to_dict() for g in guides])


@users_bp.route('/<int:uid>', methods=['GET'])
def get_user(uid):
    user = User.query.get_or_404(uid)
    return jsonify(user.to_dict())
