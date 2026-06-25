from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

# ─────────────────────────────────────────
# USER
# ─────────────────────────────────────────
class User(db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(100), unique=True, nullable=False)
    password      = db.Column(db.String(255), nullable=False)
    role          = db.Column(db.String(50), nullable=False)
    # roles: Student | Guide | HoD | External Examiner

    # Guide-specific: up to 3 domains
    domain1       = db.Column(db.String(100), nullable=True)
    domain2       = db.Column(db.String(100), nullable=True)
    domain3       = db.Column(db.String(100), nullable=True)

    # External Examiner-specific
    exam_sem      = db.Column(db.Integer, nullable=True)    # e.g. 6
    exam_year     = db.Column(db.Integer, nullable=True)    # e.g. 2026

    firebase_uid  = db.Column(db.String(200), nullable=True, unique=True)

    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    def domains_list(self):
        return [d for d in [self.domain1, self.domain2, self.domain3] if d]

    def to_dict(self):
        return {
            'id':        self.id,
            'name':      self.name,
            'email':     self.email,
            'role':      self.role,
            'domains':   self.domains_list(),
            'exam_sem':  self.exam_sem,
            'exam_year': self.exam_year,
        }


# ─────────────────────────────────────────
# PROJECT
# ─────────────────────────────────────────
class Project(db.Model):
    __tablename__ = 'projects'

    id             = db.Column(db.Integer, primary_key=True)
    title          = db.Column(db.String(200), nullable=False)
    description    = db.Column(db.Text)
    domain         = db.Column(db.String(100))          # auto-matched to guide
    project_type   = db.Column(db.String(20))           # Major / Minor
    sem            = db.Column(db.Integer)              # semester
    year           = db.Column(db.Integer)              # batch year

    github_link    = db.Column(db.String(500))
    demo_link      = db.Column(db.String(500))          # video drive link
    report_link    = db.Column(db.String(500))          # report drive link
    code_link      = db.Column(db.String(500))          # code drive link

    status         = db.Column(db.String(50), default='Ongoing')
    # Ongoing | Completed | Evaluated

    is_evaluated   = db.Column(db.Boolean, default=False)
    marks          = db.Column(db.Float, nullable=True)  # out of 50

    student_id     = db.Column(db.Integer, db.ForeignKey('users.id'))
    guide_id       = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    group_members  = db.Column(db.Text)                 # comma-separated names
    likes          = db.Column(db.Integer, default=0)

    created_at     = db.Column(db.DateTime, default=datetime.utcnow)

    student        = db.relationship('User', foreign_keys=[student_id], backref='projects')
    guide          = db.relationship('User', foreign_keys=[guide_id],   backref='guided_projects')

    def to_dict(self):
        return {
            'id':           self.id,
            'title':        self.title,
            'description':  self.description,
            'domain':       self.domain,
            'project_type': self.project_type,
            'sem':          self.sem,
            'year':         self.year,
            'github_link':  self.github_link,
            'demo_link':    self.demo_link,
            'report_link':  self.report_link,
            'code_link':    self.code_link,
            'status':       self.status,
            'is_evaluated': self.is_evaluated,
            'marks':        self.marks,
            'student_id':   self.student_id,
            'student_name': self.student.name if self.student else '',
            'guide_id':     self.guide_id,
            'guide_name':   self.guide.name if self.guide else 'Unassigned',
            'group_members': self.group_members or '',
            'likes':        self.likes,
            'created_at':   self.created_at.strftime('%Y-%m-%d') if self.created_at else '',
        }


# ─────────────────────────────────────────
# PROGRESS
# ─────────────────────────────────────────
class Progress(db.Model):
    __tablename__ = 'progress'

    id          = db.Column(db.Integer, primary_key=True)
    project_id  = db.Column(db.Integer, db.ForeignKey('projects.id'))
    week_no     = db.Column(db.Integer)
    update_text = db.Column(db.Text)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    project     = db.relationship('Project', backref='progress_logs')

    def to_dict(self):
        return {
            'id':          self.id,
            'week':        self.week_no,
            'update':      self.update_text,
            'created_at':  self.created_at.strftime('%Y-%m-%d'),
        }


# ─────────────────────────────────────────
# EVALUATION
# ─────────────────────────────────────────
class Evaluation(db.Model):
    __tablename__ = 'evaluations'

    id            = db.Column(db.Integer, primary_key=True)
    project_id    = db.Column(db.Integer, db.ForeignKey('projects.id'))
    evaluator_id  = db.Column(db.Integer, db.ForeignKey('users.id'))
    marks         = db.Column(db.Float)           # out of 50
    remarks       = db.Column(db.Text)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    project       = db.relationship('Project',  backref='evaluations')
    evaluator     = db.relationship('User',     backref='evaluations_given')

    def to_dict(self):
        return {
            'id':            self.id,
            'project_id':    self.project_id,
            'evaluator_id':  self.evaluator_id,
            'evaluator_name': self.evaluator.name if self.evaluator else '',
            'marks':         self.marks,
            'remarks':       self.remarks,
            'created_at':    self.created_at.strftime('%Y-%m-%d'),
        }


# ─────────────────────────────────────────
# COMMENT
# ─────────────────────────────────────────
class Comment(db.Model):
    __tablename__ = 'comments'

    id          = db.Column(db.Integer, primary_key=True)
    project_id  = db.Column(db.Integer, db.ForeignKey('projects.id'))
    author_id   = db.Column(db.Integer, db.ForeignKey('users.id'))
    text        = db.Column(db.Text, nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    project     = db.relationship('Project', backref='comments')
    author      = db.relationship('User',    backref='comments_made')

    def to_dict(self):
        role = self.author.role if self.author else 'Student'
        is_pinned = role in ('Guide', 'HoD', 'External Examiner')
        return {
            'id':         self.id,
            'project_id': self.project_id,
            'author_id':  self.author_id,
            'author_name': self.author.name if self.author else '',
            'author_role': role,
            'text':       self.text,
            'is_pinned':  is_pinned,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
        }


# ─────────────────────────────────────────
# PROJECT LIKE
# ─────────────────────────────────────────
class ProjectLike(db.Model):
    __tablename__ = 'project_likes'

    id          = db.Column(db.Integer, primary_key=True)
    project_id  = db.Column(db.Integer, db.ForeignKey('projects.id'))
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'))

    __table_args__ = (
        db.UniqueConstraint('project_id', 'user_id', name='unique_project_like'),
    )
