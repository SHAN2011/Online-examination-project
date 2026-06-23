from app import app
from models import Exam

with app.app_context():
    e = Exam.query.get(3)
    if e:
        print(f'Exam: {e.title}')
        print(f'Duration: {e.duration}')
        print(f'Questions: {len(e.questions)}')
        for q in e.questions:
            print(f'  - {q.question_text}')