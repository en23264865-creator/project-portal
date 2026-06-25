from flask import Blueprint, send_file
from models import db, User, Project, Evaluation
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
import io

export_bp = Blueprint('export', __name__)


def style_header(ws, headers):
    ws.append(headers)
    for cell in ws[1]:
        cell.font      = Font(bold=True, color='FFFFFF')
        cell.fill      = PatternFill('solid', fgColor='1a1a2e')
        cell.alignment = Alignment(horizontal='center')


@export_bp.route('/students')
def export_students():
    wb = Workbook()
    ws = wb.active
    ws.title = 'Students'
    style_header(ws, ['ID', 'Name', 'Email'])
    for s in User.query.filter_by(role='Student').all():
        ws.append([s.id, s.name, s.email])
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return send_file(buf, as_attachment=True,
                     download_name='students.xlsx',
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@export_bp.route('/projects')
def export_projects():
    wb = Workbook()
    ws = wb.active
    ws.title = 'Projects'
    style_header(ws, ['ID', 'Title', 'Domain', 'Type', 'Sem', 'Year',
                       'Student', 'Guide', 'Status', 'Evaluated', 'Marks'])
    for p in Project.query.all():
        ws.append([
            p.id, p.title, p.domain, p.project_type, p.sem, p.year,
            p.student.name if p.student else '',
            p.guide.name   if p.guide   else '',
            p.status, 'Yes' if p.is_evaluated else 'No',
            p.marks if p.marks else '',
        ])
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return send_file(buf, as_attachment=True,
                     download_name='projects.xlsx',
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
