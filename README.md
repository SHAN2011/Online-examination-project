# Online Examination Management System

## Features
- ✅ Role-based access (Admin/Teacher/Student)
- ✅ Complete CRUD for users and exams
- ✅ Timer-based exams with auto-submit
- ✅ Auto-grading system
- ✅ Modern Bootstrap UI with animations
- ✅ Dashboard analytics
- ✅ Responsive design

## Tech Stack
```
Backend: Flask, Flask-SQLAlchemy, Flask-Login
Frontend: Bootstrap 5, Chart.js, Custom CSS/JS
Database: SQLite3
```

## Quick Setup & Run

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Initialize database with sample data:**
```bash
python app.py init-db
```
*Sample accounts:*
- Admin: `admin@test.com` / `pass123`
- Teacher: `teacher1@test.com` / `pass123` 
- Student: `student1@test.com` / `pass123`

3. **Start the server:**
```bash
python app.py
```

4. **Open browser:** `http://127.0.0.1:5000`

## Usage

### Admin (`/admin/dashboard`)
- View analytics
- Manage teachers/students
- View all exams/results

### Teacher (`/teacher/dashboard`)
- Create exams with MCQ questions
- Assign to students
- View submissions

### Student (`/student/dashboard`)
- View assigned exams
- Take timed exams
- View results with detailed feedback

## File Structure
```
├── app.py              # Main Flask app
├── models.py           # Database models
├── config.py           # App config
├── requirements.txt
├── routes/             # Blueprint routes
├── templates/          # HTML templates
├── static/             # CSS/JS
└── README.md
```

## Testing Flow
1. Login as Admin → Add teachers/students
2. Login as Teacher → Create exam → Assign to students  
3. Login as Student → Take exam → View results
4. Admin/Teacher → View all results

**Project fully functional! 🚀**

