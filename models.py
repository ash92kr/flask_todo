from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Todo(db.Model) : 
    __tablename__ = 'todos'   # todo 테이블이 여러 개 들어가므로 복수 명이 좋다
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String, nullable=False)
    deadline = db.Column(db.DateTime)
    
    # 생성자
    def __init__(self, todo, deadline):
        self.todo = todo,
        self.deadline = deadline  # self.todo = 위쪽의 todo, todo 인자 = todo