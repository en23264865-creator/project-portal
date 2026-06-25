"""
Run once to seed the database with dummy data.
Usage: python seed.py
"""
from app import app
from models import db, bcrypt, User, Project, Progress, Evaluation, Comment

DOMAINS = [
    'AI/ML',
    'IoT',
    'Cybersecurity',
    'Web Development',
    'Data Science',
    'Blockchain',
    'Cloud Computing',
    'Mobile Development',
]

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # ── Guides (Faculty) ─────────────────────────────────────────
        guides_data = [
            dict(name='Kranti Gajmal',  email='kranti.gajmal@college.com',  d1='AI/ML',          d2='Data Science',      d3='IoT'),
            dict(name='Shradha Jadhav', email='shradha.jadhav@college.com', d1='Web Development', d2='Mobile Development',d3='Cloud Computing'),
            dict(name='Diksha Rane',    email='diksha.rane@college.com',     d1='Cybersecurity',  d2='Blockchain',        d3='IoT'),
        ]
        guides = []
        for g in guides_data:
            u = User(
                name=g['name'], email=g['email'],
                password=bcrypt.generate_password_hash('Guide@123').decode('utf-8'),
                role='Guide',
                domain1=g['d1'], domain2=g['d2'], domain3=g['d3']
            )
            db.session.add(u)
            guides.append(u)
        db.session.flush()

        # ── HoD ──────────────────────────────────────────────────────
        hod = User(
            name='Dr. HoD',
            email='hod@college.com',
            password=bcrypt.generate_password_hash('Hod@123').decode('utf-8'),
            role='HoD'
        )
        db.session.add(hod)

        # ── External Examiners ────────────────────────────────────────
        examiners_data = [
            dict(name='Nitin Mohite',     email='nitin.mohite@exam.com',     sem=6, year=2026),
            dict(name='Manali Khedekar',  email='manali.khedekar@exam.com',  sem=6, year=2026),
            dict(name='Jyoti Khalkar',    email='jyoti.khalkar@exam.com',    sem=6, year=2026),
        ]
        examiners = []
        for e in examiners_data:
            u = User(
                name=e['name'], email=e['email'],
                password=bcrypt.generate_password_hash('Exam@123').decode('utf-8'),
                role='External Examiner',
                exam_sem=e['sem'], exam_year=e['year']
            )
            db.session.add(u)
            examiners.append(u)
        db.session.flush()

        # ── Students ─────────────────────────────────────────────────
        student_names = [
            'Aarav Sharma', 'Priya Patil', 'Rohan Mehta', 'Sneha Kulkarni', 'Arjun Desai',
            'Pooja Nair',   'Vikram Joshi','Ananya Singh', 'Rahul Gupta',    'Nisha Reddy',
            'Aditya More',  'Kavya Pillai','Siddharth Rao','Meera Iyer',     'Karan Verma',
        ]
        students = []
        for i, sname in enumerate(student_names, 1):
            first = sname.split()[0].lower()
            u = User(
                name=sname,
                email=f'{first}.student{i}@college.com',
                password=bcrypt.generate_password_hash('Student@123').decode('utf-8'),
                role='Student'
            )
            db.session.add(u)
            students.append(u)
        db.session.flush()

        # ── Projects ──────────────────────────────────────────────────
        # Map domain → guide
        domain_guide_map = {}
        for g in guides:
            for d in g.domains_list():
                domain_guide_map[d] = g.id

        projects_seed = [
            dict(title='Smart Attendance System',       domain='AI/ML',          ptype='Major', desc='Face-recognition attendance using CNN.'),
            dict(title='IoT Smart Home Dashboard',      domain='IoT',            ptype='Major', desc='Control home appliances via mobile app.'),
            dict(title='Network Intrusion Detector',    domain='Cybersecurity',  ptype='Minor', desc='ML-based intrusion detection system.'),
            dict(title='College ERP Portal',            domain='Web Development',ptype='Major', desc='Full-stack ERP for college management.'),
            dict(title='Crop Yield Prediction',         domain='Data Science',   ptype='Minor', desc='Predict crop yield using historical data.'),
            dict(title='DeFi Token Exchange',           domain='Blockchain',     ptype='Major', desc='Decentralized exchange on Ethereum.'),
            dict(title='Serverless Chat App',           domain='Cloud Computing',ptype='Minor', desc='Real-time chat using AWS Lambda.'),
            dict(title='Flutter Health Tracker',        domain='Mobile Development', ptype='Major', desc='Track daily health metrics on Android/iOS.'),
            dict(title='Sentiment Analysis Engine',     domain='AI/ML',          ptype='Minor', desc='Twitter sentiment using BERT.'),
            dict(title='Smart Irrigation System',       domain='IoT',            ptype='Minor', desc='Automated irrigation with soil sensors.'),
            dict(title='Phishing URL Detector',         domain='Cybersecurity',  ptype='Major', desc='ML model to detect phishing URLs.'),
            dict(title='Online Exam Platform',          domain='Web Development',ptype='Major', desc='Proctored online exam system.'),
            dict(title='Stock Price Forecasting',       domain='Data Science',   ptype='Major', desc='LSTM model for NSE stock prediction.'),
            dict(title='NFT Marketplace',               domain='Blockchain',     ptype='Minor', desc='Mint and trade NFTs on Polygon.'),
            dict(title='CI/CD Pipeline Tool',           domain='Cloud Computing',ptype='Minor', desc='Automated deployment using Docker & GitHub Actions.'),
        ]

        group_members_pool = [s.name for s in students]

        for idx, pd in enumerate(projects_seed):
            guide_id = domain_guide_map.get(pd['domain'])
            s = students[idx % len(students)]
            # pick 2 group members
            m1 = group_members_pool[(idx + 1) % len(group_members_pool)]
            m2 = group_members_pool[(idx + 2) % len(group_members_pool)]
            members = f"{s.name}, {m1}, {m2}"

            is_evaluated = idx < 6
            project = Project(
                title=pd['title'],
                description=pd['desc'],
                domain=pd['domain'],
                project_type=pd['ptype'],
                sem=6,
                year=2026,
                github_link=f'https://github.com/student{idx+1}/{pd["title"].replace(" ", "-").lower()}',
                demo_link=f'https://drive.google.com/file/d/demo_{idx+1}',
                report_link=f'https://drive.google.com/file/d/report_{idx+1}',
                code_link=f'https://drive.google.com/file/d/code_{idx+1}',
                status='Evaluated' if is_evaluated else ('Completed' if idx < 10 else 'Ongoing'),
                is_evaluated=is_evaluated,
                marks=round(35 + (idx * 2.3) % 15, 1) if is_evaluated else None,
                student_id=s.id,
                guide_id=guide_id,
                group_members=members,
                likes=idx * 3,
            )
            db.session.add(project)
        db.session.flush()

        # ── Progress logs ─────────────────────────────────────────────
        all_projects = Project.query.all()
        for p in all_projects[:8]:
            for w in range(1, 5):
                prog = Progress(
                    project_id=p.id,
                    week_no=w,
                    update_text=f'Week {w}: Completed module {w} of {p.title}. All tests passing.'
                )
                db.session.add(prog)

        # ── Evaluations ───────────────────────────────────────────────
        evaluated_projects = Project.query.filter_by(is_evaluated=True).all()
        ex = examiners[0]
        for p in evaluated_projects:
            ev = Evaluation(
                project_id=p.id,
                evaluator_id=ex.id,
                marks=p.marks,
                remarks=f'Good work on {p.title}. Presentation was clear and well-structured.'
            )
            db.session.add(ev)

        # ── Comments ──────────────────────────────────────────────────
        for p in all_projects[:5]:
            # Guide comment (pinned)
            if p.guide_id:
                c = Comment(project_id=p.id, author_id=p.guide_id,
                            text=f'Great progress on {p.title}. Keep up the documentation.')
                db.session.add(c)
            # HoD comment (pinned)
            c2 = Comment(project_id=p.id, author_id=hod.id,
                         text=f'Reviewed {p.title} — ensure timelines are met.')
            db.session.add(c2)
            # Student comment
            c3 = Comment(project_id=p.id, author_id=p.student_id,
                         text='Thank you for the feedback. We will update accordingly.')
            db.session.add(c3)

        db.session.commit()
        print('✅ Database seeded successfully.')
        print('\n── Login Credentials ──────────────────────────────────')
        print('Students:         student.name@college.com / Student@123')
        print('Guides:           kranti.gajmal@college.com / Guide@123')
        print('                  shradha.jadhav@college.com / Guide@123')
        print('                  diksha.rane@college.com / Guide@123')
        print('HoD:              hod@college.com / Hod@123')
        print('External Exams:   nitin.mohite@exam.com / Exam@123')
        print('                  manali.khedekar@exam.com / Exam@123')
        print('                  jyoti.khalkar@exam.com / Exam@123')

if __name__ == '__main__':
    seed()
