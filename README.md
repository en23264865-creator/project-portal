# 🎓 Project Portal — BE Final Year

A full-stack Flask + PostgreSQL web application for managing BE final-year projects.  
Built for the Department of Computer Engineering — UI/UX domain.

---

## 📁 Project Structure

```
project_portal/
├── app.py              # Flask app factory + entry point
├── config.py           # Config (DB URL, JWT secret)
├── models.py           # SQLAlchemy models (User, Project, Progress, Evaluation, Comment)
├── seed.py             # Dummy data seeder
├── requirements.txt
├── Procfile            # For Render / Heroku
├── .env.example        # Environment variable template
├── routes/
│   ├── auth.py         # /auth/register  /auth/login
│   ├── projects.py     # /projects  (CRUD, like, search, stats)
│   ├── users.py        # /users/me  /users/guides
│   ├── evaluations.py  # /evaluations
│   ├── progress.py     # /progress
│   ├── comments.py     # /comments
│   └── export.py       # /export/students  /export/projects
└── templates/
    └── index.html      # Single-page frontend
```

---

## 🚀 Run Locally

### 1. Prerequisites
- Python 3.10+
- PostgreSQL installed and running

### 2. Create a PostgreSQL database
```sql
CREATE DATABASE project_portal;
```

### 3. Clone and set up
```bash
git clone <your-repo-url>
cd project_portal

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env — set DATABASE_URL and JWT_SECRET_KEY
```

`.env` example:
```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/project_portal
JWT_SECRET_KEY=my_super_secret_key_1234
```

### 5. Seed the database
```bash
python seed.py
```
This creates all tables and inserts dummy users, projects, progress logs, evaluations, and comments.

### 6. Run the server
```bash
python app.py
```
Open → http://localhost:5000

---

## 🔑 Demo Login Credentials

| Role              | Email                          | Password     |
|-------------------|--------------------------------|--------------|
| Student           | aarav.student1@college.com     | Student@123  |
| Guide             | kranti.gajmal@college.com      | Guide@123    |
| Guide             | shradha.jadhav@college.com     | Guide@123    |
| Guide             | diksha.rane@college.com        | Guide@123    |
| HoD               | hod@college.com                | Hod@123      |
| External Examiner | nitin.mohite@exam.com          | Exam@123     |
| External Examiner | manali.khedekar@exam.com       | Exam@123     |
| External Examiner | jyoti.khalkar@exam.com         | Exam@123     |

---

## ☁️ Deploy on Render (Free Tier)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/project-portal.git
git push -u origin main
```

### Step 2 — Create a PostgreSQL database on Render
1. Go to https://render.com → **New** → **PostgreSQL**
2. Choose the free plan, pick a name, click **Create**
3. Copy the **Internal Database URL** (starts with `postgresql://`)

### Step 3 — Create a Web Service on Render
1. **New** → **Web Service**
2. Connect your GitHub repo
3. Settings:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Under **Environment Variables**, add:
   - `DATABASE_URL` → paste the PostgreSQL URL from Step 2
   - `JWT_SECRET_KEY` → any long random string

### Step 4 — Seed the database (once)
After the first deploy, go to **Shell** in Render dashboard and run:
```bash
python seed.py
```

### Step 5 — Visit your app
Render gives you a URL like `https://project-portal-xxxx.onrender.com` 🎉

---

## 🌟 Features

| Feature                      | Details |
|-----------------------------|---------|
| 🎯 Auto Guide Assignment     | Domain-matched — student picks domain, guide auto-assigned |
| 🧑‍🎓 Student Portal           | Submit projects, log weekly progress, like projects |
| 🧑‍🏫 Guide Portal             | View students, their projects, and progress timelines |
| 📝 External Examiner Portal  | Evaluate projects for assigned sem & batch year (marks / 50) |
| 🏛️ HoD Portal               | See all projects, export Excel sheets |
| 💬 Pinned Comments           | Guide / HoD / Examiner comments always pinned at top |
| 📈 Progress Timeline         | Week-by-week visual timeline per project |
| ❤️ Like System               | One like per user per project |
| 📥 Excel Export              | Styled .xlsx files for students and projects |
| 🔒 JWT Auth                  | Secure token-based authentication |

---

## 🛠️ Tech Stack

- **Backend**: Flask, SQLAlchemy, Flask-JWT-Extended, Flask-Bcrypt
- **Database**: PostgreSQL (SQLite for local dev if you change DATABASE_URL)
- **Frontend**: Vanilla HTML/CSS/JS (single-page app inside `templates/index.html`)
- **Deploy**: Render (gunicorn)
