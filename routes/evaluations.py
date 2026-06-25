from flask import Blueprint, request, jsonify
from models import db, User, Project, Evaluation
from flask_jwt_extended import jwt_required, get_jwt_identity

evaluations_bp = Blueprint('evaluations', __name__)


@evaluations_bp.route('', methods=['POST'])
@jwt_required()
def evaluate():
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)

    if user.role not in ('External Examiner',):
        return jsonify({'message': 'Only External Examiners can evaluate'}), 403

    data = request.json
    project_id = data.get('project_id')
    marks      = data.get('marks')
    remarks    = data.get('remarks', '')

    if marks is None or not (0 <= float(marks) <= 50):
        return jsonify({'message': 'Marks must be between 0 and 50'}), 400

    project = Project.query.get_or_404(project_id)
    if project.sem != user.exam_sem or project.year != user.exam_year:
        return jsonify({'message': 'Project not in your assigned batch'}), 403

    # Overwrite if already evaluated
    existing = Evaluation.query.filter_by(project_id=project_id, evaluator_id=user_id).first()
    if existing:
        existing.marks   = float(marks)
        existing.remarks = remarks
    else:
        ev = Evaluation(
            project_id   = project_id,
            evaluator_id = user_id,
            marks        = float(marks),
            remarks      = remarks,
        )
        db.session.add(ev)

    project.marks        = float(marks)
    project.is_evaluated = True
    project.status       = 'Evaluated'
    db.session.commit()

    return jsonify({'message': 'Evaluation saved', 'marks': marks})


@evaluations_bp.route('/project/<int:pid>', methods=['GET'])
def get_evaluations(pid):
    evals = Evaluation.query.filter_by(project_id=pid).all()
    return jsonify([e.to_dict() for e in evals])
