"""
Seed the database with dummy data.
Usage:  python seed.py
Auto-called from app.py on first boot if DB is empty.
"""

DOMAINS = [
    'AI/ML', 'IoT', 'Cybersecurity', 'Web Development',
    'Data Science', 'Blockchain', 'Cloud Computing', 'Mobile Development',
]

# ── guide domain assignments ──────────────────────────────────────────────────
GUIDE_DATA = [
    {
        'name': 'Kranti Gajmal',
        'email': 'kranti.gajmal@college.com',
        'contact': '9876543201',
        'password': 'Guide@123',
        'domains': ['AI/ML', 'Data Science', 'IoT']
    },
    {
        'name': 'Shradha Jadhav',
        'email': 'shradha.jadhav@college.com',
        'contact': '9876543202',
        'password': 'Guide@123',
        'domains': ['Web Development', 'Mobile Development', 'Cloud Computing']
    },
    {
        'name': 'Diksha Rane',
        'email': 'diksha.rane@college.com',
        'contact': '9876543203',
        'password': 'Guide@123',
        'domains': ['Cybersecurity', 'Blockchain', 'IoT']
    }
]

# ── students ──────────────────────────────────────────────────────────────────
STUDENT_DATA = [
    ('Aarav Sharma', 'aarav.sharma@college.com', '9876543210'),
    ('Priya Patil', 'priya.patil@college.com', '9876543211'),
    ('Rohan Mehta', 'rohan.mehta@college.com', '9876543212'),
    ('Sneha Kulkarni', 'sneha.kulkarni@college.com', '9876543213'),
    ('Arjun Desai', 'arjun.desai@college.com', '9876543214'),
    ('Pooja Nair', 'pooja.nair@college.com', '9876543215'),
    ('Vikram Joshi', 'vikram.joshi@college.com', '9876543216'),
    ('Ananya Singh', 'ananya.singh@college.com', '9876543217'),
    ('Rahul Gupta', 'rahul.gupta@college.com', '9876543218'),
    ('Nisha Reddy', 'nisha.reddy@college.com', '9876543219'),
    ('Aditya More', 'aditya.more@college.com', '9876543220'),
    ('Kavya Pillai', 'kavya.pillai@college.com', '9876543221'),
    ('Siddharth Rao', 'siddharth.rao@college.com', '9876543222'),
    ('Meera Iyer', 'meera.iyer@college.com', '9876543223'),
    ('Karan Verma', 'karan.verma@college.com', '9876543224')
]

# ── projects ──────────────────────────────────────────────────────────────────
PROJECT_DATA = [
    dict(
        title='Smart Attendance System',
        domain='AI/ML', ptype='Major',
        desc='Face-recognition based attendance system using CNN and OpenCV. '
             'Automatically marks present when a registered face is detected via webcam.',
        members=['Aarav Sharma', 'Priya Patil', 'Rohan Mehta'],
        status='Evaluated', marks=46.0,
    ),
    dict(
        title='IoT Smart Home Dashboard',
        domain='IoT', ptype='Major',
        desc='Control and monitor home appliances remotely via a mobile app. '
             'Uses ESP32 microcontrollers and MQTT protocol for real-time control.',
        members=['Sneha Kulkarni', 'Arjun Desai', 'Pooja Nair'],
        status='Evaluated', marks=43.5,
    ),
    dict(
        title='Network Intrusion Detection System',
        domain='Cybersecurity', ptype='Minor',
        desc='ML-based system that detects anomalous network traffic patterns '
             'using Random Forest classifier trained on the KDD Cup dataset.',
        members=['Vikram Joshi', 'Ananya Singh', 'Rahul Gupta'],
        status='Evaluated', marks=41.0,
    ),
    dict(
        title='College ERP Portal',
        domain='Web Development', ptype='Major',
        desc='Full-stack web application for college management covering admissions, '
             'attendance, fees, timetable and results. Built with React and Node.js.',
        members=['Nisha Reddy', 'Aditya More', 'Kavya Pillai'],
        status='Evaluated', marks=44.5,
    ),
    dict(
        title='Crop Yield Prediction using ML',
        domain='Data Science', ptype='Minor',
        desc='Predicts crop yield based on soil type, weather data and historical records '
             'using XGBoost. Achieved 92% accuracy on test data.',
        members=['Siddharth Rao', 'Meera Iyer', 'Karan Verma'],
        status='Evaluated', marks=39.5,
    ),
    dict(
        title='DeFi Token Exchange',
        domain='Blockchain', ptype='Major',
        desc='Decentralized cryptocurrency exchange built on Ethereum using Solidity smart '
             'contracts. Supports ERC-20 token swaps with MetaMask wallet integration.',
        members=['Aarav Sharma', 'Vikram Joshi', 'Siddharth Rao'],
        status='Evaluated', marks=47.0,
    ),
    dict(
        title='Serverless Chat Application',
        domain='Cloud Computing', ptype='Minor',
        desc='Real-time chat app using AWS Lambda, API Gateway and DynamoDB. '
             'Supports group chats, file sharing and end-to-end encryption.',
        members=['Priya Patil', 'Ananya Singh', 'Meera Iyer'],
        status='Completed', marks=None,
    ),
    dict(
        title='Flutter Health Tracker',
        domain='Mobile Development', ptype='Major',
        desc='Cross-platform mobile app that tracks daily health metrics including '
             'steps, sleep, water intake and heart rate using device sensors and BLE.',
        members=['Rohan Mehta', 'Nisha Reddy', 'Karan Verma'],
        status='Completed', marks=None,
    ),
    dict(
        title='Sentiment Analysis Engine',
        domain='AI/ML', ptype='Minor',
        desc='Twitter sentiment analysis using fine-tuned BERT model. '
             'Classifies tweets into positive, negative and neutral with 89% accuracy.',
        members=['Sneha Kulkarni', 'Rahul Gupta', 'Aditya More'],
        status='Completed', marks=None,
    ),
    dict(
        title='Smart Irrigation System',
        domain='IoT', ptype='Minor',
        desc='Automated drip irrigation system with soil moisture sensors and '
             'weather API integration. Reduces water usage by up to 40%.',
        members=['Arjun Desai', 'Kavya Pillai', 'Pooja Nair'],
        status='Completed', marks=None,
    ),
    dict(
        title='Phishing URL Detector',
        domain='Cybersecurity', ptype='Major',
        desc='Browser extension powered by an ML model that flags suspicious URLs in '
             'real time. Trained on a dataset of 100k+ URLs with 96% precision.',
        members=['Vikram Joshi', 'Meera Iyer', 'Aarav Sharma'],
        status='Ongoing', marks=None,
    ),
    dict(
        title='Online Proctored Exam Platform',
        domain='Web Development', ptype='Major',
        desc='AI-powered online exam platform with face detection, tab-switch alerts, '
             'and auto-grading. Built with Django, WebRTC and TensorFlow.js.',
        members=['Nisha Reddy', 'Siddharth Rao', 'Priya Patil'],
        status='Ongoing', marks=None,
    ),
    dict(
        title='Stock Price Forecasting with LSTM',
        domain='Data Science', ptype='Major',
        desc='Deep learning model using LSTM networks to forecast NSE stock prices. '
             'Integrates live data from Yahoo Finance API with an interactive dashboard.',
        members=['Karan Verma', 'Ananya Singh', 'Rohan Mehta'],
        status='Ongoing', marks=None,
    ),
    dict(
        title='NFT Marketplace on Polygon',
        domain='Blockchain', ptype='Minor',
        desc='Platform to mint, buy and sell NFTs on the Polygon blockchain. '
             'Supports ERC-721 tokens, IPFS storage and Metamask/WalletConnect.',
        members=['Aditya More', 'Rahul Gupta', 'Sneha Kulkarni'],
        status='Ongoing', marks=None,
    ),
    dict(
        title='CI/CD Pipeline Automation Tool',
        domain='Cloud Computing', ptype='Minor',
        desc='A GitHub Actions-based CI/CD tool with Docker containerisation, '
             'automated testing, staging deployment and Slack notifications.',
        members=['Kavya Pillai', 'Arjun Desai', 'Vikram Joshi'],
        status='Ongoing', marks=None,
    ),
]

# ── progress updates per project ──────────────────────────────────────────────
PROGRESS_UPDATES = [
    'Completed literature review and finalized project scope. Tech stack decided.',
    'Set up development environment. Created initial project structure and GitHub repo.',
    'Implemented core module. Basic functionality working. Unit tests written.',
    'Integrated all modules. UI completed. Bug fixes and performance improvements done.',
    'Final testing done. Documentation written. Project ready for submission.',
]


def seed():
    from models import db, bcrypt, User, Project, Progress, Evaluation, Comment

    print("📋 Seeding database...")

    # ── Step 1: Create Guides ─────────────────────────────────────────────────
    guide_objects = []
    for g in GUIDE_DATA:
        user = User(
            name     = g['name'],
            email    = g['email'],
            contact  = g['contact'],
            password = bcrypt.generate_password_hash(g['password']).decode('utf-8'),
            role     = 'Guide',
            domain1  = g['domains'][0],
            domain2  = g['domains'][1],
            domain3  = g['domains'][2] if len(g['domains']) > 2 else None,
        )
        db.session.add(user)
        guide_objects.append((user, g['domains']))

    db.session.commit()   # commit so IDs are assigned
    print(f'✅ {len(guide_objects)} guides created.')

    # ── Step 2: Build domain → guide_id map ──────────────────────────────────
    domain_guide_map = {}
    for user, domains in guide_objects:
        for d in domains:
            domain_guide_map[d] = user.id

    # ── Step 3: Create HoD ───────────────────────────────────────────────────
    hod = User(
        name     = 'Dr. HoD',
        email    = 'hod@college.com',
        contact  = '9876543204',
        password = bcrypt.generate_password_hash('Hod@123').decode('utf-8'),
        role     = 'HoD',
    )
    db.session.add(hod)
    db.session.commit()
    print('✅ HoD created.')

    # ── Step 4: Create External Examiners ────────────────────────────────────
    examiners_raw = [
        ('Nitin Mohite', 'nitin.mohite@exam.com', '9876543205', 'Exam@123', 6, 2026),
        ('Manali Khedekar', 'manali.khedekar@exam.com', '9876543206', 'Exam@123', 6, 2026),
        ('Jyoti Khalkar', 'jyoti.khalkar@exam.com', '9876543207', 'Exam@123', 6, 2026),
        ]
    examiner_objects = []
    for name, email, contact, pwd, sem, year in examiners_raw:
        u = User(
            name      = name,
            email     = email,
            contact   = contact,
            password  = bcrypt.generate_password_hash(pwd).decode('utf-8'),
            role      = 'External Examiner',
            exam_sem  = sem,
            exam_year = year,
        )
        db.session.add(u)
        examiner_objects.append(u)
    db.session.commit()
    print(f'✅ {len(examiner_objects)} examiners created.')

    # ── Step 5: Create Students ───────────────────────────────────────────────
    student_objects = []
    for name, email, contact in STUDENT_DATA:
        u = User(
            name     = name,
            email    = email,
            contact  = contact,
            password = bcrypt.generate_password_hash('Student@123').decode('utf-8'),
            role     = 'Student',
        )
        db.session.add(u)
        student_objects.append(u)
    db.session.commit()
    print(f'✅ {len(student_objects)} students created.')

    # Build name → student_id map
    student_map = {u.name: u.id for u in student_objects}

    # ── Step 6: Create Projects ───────────────────────────────────────────────
    project_objects = []
    for idx, pd in enumerate(PROJECT_DATA):
        guide_id   = domain_guide_map.get(pd['domain'])
        lead_name  = pd['members'][0]
        student_id = student_map.get(lead_name, student_objects[idx % len(student_objects)].id)
        members_str = ', '.join(pd['members'])

        p = Project(
            title         = pd['title'],
            description   = pd['desc'],
            domain        = pd['domain'],
            project_type  = pd['ptype'],
            sem           = 6,
            year          = 2026,
            github_link   = f'https://github.com/{lead_name.split()[0].lower()}/{pd["title"].replace(" ", "-").lower()}',
            demo_link     = f'https://drive.google.com/file/d/demo_{idx+1}/view',
            report_link   = f'https://drive.google.com/file/d/report_{idx+1}/view',
            code_link     = f'https://drive.google.com/file/d/code_{idx+1}/view',
            status        = pd['status'],
            is_evaluated  = pd['status'] == 'Evaluated',
            marks         = pd['marks'],
            student_id    = student_id,
            guide_id      = guide_id,
            group_members = members_str,
            likes         = (idx + 1) * 4,
        )
        db.session.add(p)
        project_objects.append(p)

    db.session.commit()
    print(f'✅ {len(project_objects)} projects created.')

    # ── Step 7: Progress logs ────────────────────────────────────────────────
    for idx, p in enumerate(project_objects):
        num_weeks = 5 if p.status == 'Evaluated' else (4 if p.status == 'Completed' else 2)
        for w in range(1, num_weeks + 1):
            update = PROGRESS_UPDATES[w - 1] if w <= len(PROGRESS_UPDATES) else f'Week {w}: Work in progress.'
            db.session.add(Progress(
                project_id  = p.id,
                week_no     = w,
                update_text = f'Week {w} — {p.title}: {update}',
            ))
    db.session.commit()
    print('✅ Progress logs created.')

    # ── Step 8: Evaluations (for evaluated projects) ─────────────────────────
    evaluated = [p for p in project_objects if p.is_evaluated]
    ex = examiner_objects[0]
    for p in evaluated:
        db.session.add(Evaluation(
            project_id   = p.id,
            evaluator_id = ex.id,
            marks        = p.marks,
            remarks      = (
                f'Project "{p.title}" demonstrated excellent understanding of {p.domain}. '
                f'The implementation was clean and well-documented. '
                f'Presentation was confident and questions were handled well. '
                f'Marks awarded: {p.marks}/50.'
            ),
        ))
    db.session.commit()
    print(f'✅ {len(evaluated)} evaluations created.')

    # ── Step 9: Comments ─────────────────────────────────────────────────────
    guide_map = {(u.id): u for u, _ in guide_objects}

    comment_data = [
        # (role, text_template)
        ('guide',    'Great work on {title}. Make sure the documentation is complete before submission.'),
        ('hod',      '{title} is progressing well. Ensure all deliverables are on schedule.'),
        ('student',  'Thank you for the feedback! We will incorporate these suggestions by next week.'),
        ('examiner', 'Reviewed {title}. The technical depth is impressive. Minor improvements needed in the report format.'),
    ]

    for p in project_objects[:10]:   # add comments to first 10 projects
        # Guide comment
        if p.guide_id:
            db.session.add(Comment(
                project_id = p.id,
                author_id  = p.guide_id,
                text       = f'Great work on {p.title}. Make sure the documentation is complete before submission.',
            ))
        # HoD comment
        db.session.add(Comment(
            project_id = p.id,
            author_id  = hod.id,
            text       = f'{p.title} is progressing well. Ensure all deliverables are on schedule.',
        ))
        # Student comment
        db.session.add(Comment(
            project_id = p.id,
            author_id  = p.student_id,
            text       = 'Thank you for the feedback! We will incorporate these suggestions by next week.',
        ))
        # Examiner comment on evaluated projects
        if p.is_evaluated:
            db.session.add(Comment(
                project_id = p.id,
                author_id  = examiner_objects[0].id,
                text       = f'Reviewed {p.title}. The technical depth is impressive. Minor improvements needed in the report format.',
            ))

    db.session.commit()
    print('✅ Comments created.')

    # ── Done ─────────────────────────────────────────────────────────────────
    print('\n' + '='*55)
    print('✅ DATABASE SEEDED SUCCESSFULLY')
    print('='*55)
    print('\n📋 LOGIN CREDENTIALS')
    print('-'*55)
    print('STUDENTS (password: Student@123)')
    for name, email, contact in STUDENT_DATA:
        print(f'  {email}')
    print('\nGUIDES (password: Guide@123)')
    for g in GUIDE_DATA:
        print(f'  {g["email"]}')
    print('\nHOD')
    print('  hod@college.com  /  Hod@123')
    print('\nEXTERNAL EXAMINERS (password: Exam@123)')
    for _, email, _, _, _, _ in examiners_raw:
        print(f'  {email}')
    print('='*55)


if __name__ == '__main__':
    # Run standalone: python seed.py
    # Creates its own Flask app — no circular import
    import os
    from flask import Flask
    from config import Config
    from models import db, bcrypt

    _app = Flask(__name__)
    _app.config.from_object(Config)
    db.init_app(_app)
    bcrypt.init_app(_app)

    with _app.app_context():
        db.create_all()
        seed()

        from models import User, Project
        if Project.query.count() == 0:
            print("🌱 Running seed...")
            from seed import seed
            seed()

        print("================================")
        print("Users:", User.query.count())
        print("Projects:", Project.query.count())
        print("================================")
