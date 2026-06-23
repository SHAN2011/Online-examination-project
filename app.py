from flask import Flask, redirect, url_for, abort
from flask_login import LoginManager, login_required, current_user
from config import Config
from models import db
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.teacher_routes import teacher_bp
from routes.student_routes import student_bp
from utils.decorators import admin_required, teacher_required, student_required

# Decorator functions
def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def teacher_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ['teacher', 'admin']:
            abort(403)
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def student_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ['student', 'admin']:
            abort(403)
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(teacher_bp, url_prefix='/teacher')
    app.register_blueprint(student_bp, url_prefix='/student')

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif current_user.role == 'teacher':
                return redirect(url_for('teacher.dashboard'))
            elif current_user.role == 'student':
                return redirect(url_for('student.dashboard'))
        return redirect(url_for('auth.login'))

    return app

app = create_app()

@app.cli.command('init-db')
def init_db():
    """Initialize database with tables and sample data."""
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Sample users
        from models import User
        admin = User(name='Admin User', email='admin@test.com', role='admin')
        admin.set_password('pass123')
        db.session.add(admin)

        teacher1 = User(name='Teacher One', email='teacher1@test.com', role='teacher')
        teacher1.set_password('pass123')
        db.session.add(teacher1)

        student1 = User(name='Student One', email='student1@test.com', role='student')
        student1.set_password('pass123')
        db.session.add(student1)

        student2 = User(name='Student Two', email='student2@test.com', role='student')
        student2.set_password('pass123')
        db.session.add(student2)

        db.session.commit()
        print("Database initialized with sample data!")
        print("Test accounts:")
        print("   Admin: admin@test.com / pass123")
        print("   Teacher: teacher1@test.com / pass123")
        print("   Student: student1@test.com / pass123")

if __name__ == '__main__':
    app.run(debug=True)

