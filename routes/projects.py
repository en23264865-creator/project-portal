from flask import Blueprint, request, jsonify
from models import db, User, Project, ProjectLike
from flask_jwt_extended import jwt_required, get_jwt_identity

projects_bp = Blueprint('projects', __name__)


def find_guide_for_domain(domain):
    """Return the first guide whose domains include the given domain."""
    guides = User.query.filter_by(role='Guide').all()
    for g in guides:
        if domain in g.domains_list():
            return g.id
    return None


@projects_bp.route('', methods=['GET'])
def get_all_projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return jsonify([p.to_dict() for p in projects])


@projects_bp.route('/<int:pid>', methods=['GET'])
def get_project(pid):
    p = Project.query.get_or_404(pid)
    return jsonify(p.to_dict())


@projects_bp.route('', methods=['POST'])
@jwt_required()
def add_project():
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)

    if user.role not in ('Student',):
        return jsonify({'message': 'Only students can submit projects'}), 403

    data = request.json
    required = ['title', 'description', 'domain', 'project_type', 'sem', 'year']
    for f in required:
        if not data.get(f):
            return jsonify({'message': f'{f} is required'}), 400

    guide_id = find_guide_for_domain(data['domain'])

    project = Project(
        title        = data['title'],
        description  = data['description'],
        domain       = data['domain'],
        project_type = data['project_type'],
        sem          = data['sem'],
        year         = data['year'],
        github_link  = data.get('github_link', ''),
        demo_link    = data.get('demo_link', ''),
        report_link  = data.get('report_link', ''),
        code_link    = data.get('code_link', ''),
        student_id   = user_id,
        guide_id     = guide_id,
        group_members= data.get('group_members', user.name),
        status       = 'Ongoing',
    )
    db.session.add(project)
    db.session.commit()

    return jsonify({
        'message':    'Project submitted successfully',
        'project':    project.to_dict(),
        'guide_name': project.guide.name if project.guide else 'No guide found for domain',
    }), 201


@projects_bp.route('/<int:pid>', methods=['PUT'])
@jwt_required()
def update_project(pid):
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)
    project = Project.query.get_or_404(pid)

    # Only the student owner or a guide can update
    if user.role == 'Student' and project.student_id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.json
    fields = ['title', 'description', 'domain', 'project_type',
              'github_link', 'demo_link', 'report_link', 'code_link',
              'status', 'group_members', 'sem', 'year']
    for f in fields:
        if f in data:
            setattr(project, f, data[f])

    # If domain changed, reassign guide
    if 'domain' in data:
        project.guide_id = find_guide_for_domain(data['domain'])

    db.session.commit()
    return jsonify({'message': 'Project updated', 'project': project.to_dict()})


@projects_bp.route('/my', methods=['GET'])
@jwt_required()
def my_projects():
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)

    if user.role == 'Student':
        projects = Project.query.filter_by(student_id=user_id).all()
    elif user.role == 'Guide':
        projects = Project.query.filter_by(guide_id=user_id).all()
    elif user.role == 'HoD':
        projects = Project.query.all()
    elif user.role == 'External Examiner':
        projects = Project.query.filter_by(
            sem=user.exam_sem, year=user.exam_year
        ).all()
    else:
        projects = []

    return jsonify([p.to_dict() for p in projects])


@projects_bp.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('q', '')
    domain  = request.args.get('domain', '')
    status  = request.args.get('status', '')
    sem     = request.args.get('sem', '')
    year    = request.args.get('year', '')

    q = Project.query
    if keyword:
        q = q.filter(Project.title.ilike(f'%{keyword}%'))
    if domain:
        q = q.filter(Project.domain == domain)
    if status:
        q = q.filter(Project.status == status)
    if sem:
        q = q.filter(Project.sem == int(sem))
    if year:
        q = q.filter(Project.year == int(year))

    projects = q.order_by(Project.created_at.desc()).all()
    return jsonify([p.to_dict() for p in projects])


@projects_bp.route('/<int:pid>/like', methods=['POST'])
@jwt_required()
def toggle_like(pid):
    user_id = int(get_jwt_identity())
    project = Project.query.get_or_404(pid)

    existing = ProjectLike.query.filter_by(project_id=pid, user_id=user_id).first()
    if existing:
        db.session.delete(existing)
        project.likes = max(0, project.likes - 1)
        liked = False
    else:
        db.session.add(ProjectLike(project_id=pid, user_id=user_id))
        project.likes += 1
        liked = True

    db.session.commit()
    return jsonify({'liked': liked, 'likes': project.likes})


@projects_bp.route('/stats', methods=['GET'])
def stats():
    from models import Evaluation
    return jsonify({
        'students':    User.query.filter_by(role='Student').count(),
        'guides':      User.query.filter_by(role='Guide').count(),
        'projects':    Project.query.count(),
        'evaluations': Evaluation.query.count(),
        'ongoing':     Project.query.filter_by(status='Ongoing').count(),
        'completed':   Project.query.filter_by(status='Completed').count(),
        'evaluated':   Project.query.filter_by(status='Evaluated').count(),
    })
