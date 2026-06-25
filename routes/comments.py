from flask import Blueprint, request, jsonify
from models import db, User, Comment
from flask_jwt_extended import jwt_required, get_jwt_identity

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('', methods=['POST'])
@jwt_required()
def add_comment():
    user_id = int(get_jwt_identity())
    data    = request.json

    c = Comment(
        project_id = data['project_id'],
        author_id  = user_id,
        text       = data['text'],
    )
    db.session.add(c)
    db.session.commit()
    return jsonify({'message': 'Comment added', 'comment': c.to_dict()}), 201


@comments_bp.route('/project/<int:pid>', methods=['GET'])
def get_comments(pid):
    comments = Comment.query.filter_by(project_id=pid).order_by(Comment.created_at).all()
    pinned = [c.to_dict() for c in comments if c.to_dict()['is_pinned']]
    others = [c.to_dict() for c in comments if not c.to_dict()['is_pinned']]
    return jsonify({'pinned': pinned, 'others': others})
