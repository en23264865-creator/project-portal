from flask import Blueprint, request, jsonify
from models import db, User, Progress
from flask_jwt_extended import jwt_required, get_jwt_identity

progress_bp = Blueprint('progress', __name__)


@progress_bp.route('', methods=['POST'])
@jwt_required()
def add_progress():
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)

    if user.role != 'Student':
        return jsonify({'message': 'Only students can log progress'}), 403

    data = request.json
    prog = Progress(
        project_id  = data['project_id'],
        week_no     = data['week_no'],
        update_text = data['update_text'],
    )
    db.session.add(prog)
    db.session.commit()
    return jsonify({'message': 'Progress logged', 'entry': prog.to_dict()}), 201


@progress_bp.route('/project/<int:pid>', methods=['GET'])
def get_progress(pid):
    logs = Progress.query.filter_by(project_id=pid).order_by(Progress.week_no).all()
    return jsonify([l.to_dict() for l in logs])
