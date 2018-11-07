from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import *
import os

app = Flask(__name__)   # app에 대한 전체 설정을 Flask로 실시

# db 설정
# app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///todo'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(('DATABASE_URL'))   # 배포용
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db.init_app(app)   # models.py에서 설정한 db를 가져옴
migrate = Migrate(app, db)


@app.route("/")
def index():
    todos = Todo.query.order_by(Todo.deadline.asc()).all()
    return render_template('index.html', todos=todos)


# 사용자가 새로운 정보를 입력하려고 함
# @app.route('/posts/new')
# def new():
#     return render_template('new.html')


# CREATE - 사용자가 보낸 데이터를 받아와 post로 만든 뒤, 이를 저장한 다음, 사용자에게 redirect를 보냄
# @app.route('/posts/create', methods=['POST'])
# def create():
    # 사용자가 입력한 폼데이터 가져오기 - new.html의 input 태그에 name을 지정해주어야 가져올 수 있다
    # todo = request.form['todo']
    # deadline = request.form.get('deadline')

    # 가져온 데이터로 Todo 만들기
    # todo = Todo(todo, deadline)   # models.py의 생성자에 todo를 생성할 때, todo/deadline만 적는다
                                  # class 안의 생성자는 첫 번째 인자가 자기 자신이어야 한다(인스턴스 생성 시 self 생략 가능)
    # Todo(todo=todo, deadline=deadline)

    # Todo DB에 저장하기
    # db.session.add(todo)
    # db.session.commit()

    # 어느 페이지로 이동할 것인가?
    # return redirect('/')
    

# 2개의 로직(create, new) 하나로 합치기
@app.route('/todos/create', methods=['POST', 'GET'])  # create 요청을 받으면 get방식과 post 방식 둘 다 받을 수 있다
def todo():
    if request.method == "POST":
        # 데이터 저장하는 로직(create)
        todo = Todo(request.form['todo'], request.form['deadline'])  # 위 todo/deadline을 1줄로 줄인 것
        db.session.add(todo)
        db.session.commit()  # 실제 데이터 베이스에 반영함
        return redirect('/')
        
    return render_template('new.html')  # new.html은 get 방식으로 받기 때문


# 삭제하는 경로를 라우트에 추가한다
# 몇 번 글을 삭제할지 알아낸다
# 글을 삭제한다
# 상태를 저장한다
# url을 어디로 보낼지 설정한다
@app.route('/todos/<int:id>/delete')   # 어떤 숫자가 들어올 지 적어야 한다
def delete(id):
    todo = Todo.query.get(id)   # id에 해당하는 번호를 찾아내 삭제
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
    
    
# edit 처리 로직
# edit하는 경로를 라우트에 추가한다.
# 기존의 데이터를 가져와서 수정할 수 있는 폼 보여주기
# @app.route('/todos/<int:id>/edit')   # get 방식으로 받음
# def edit(id):
#     todo = Todo.query.get(id)
#     return render_template('edit.html', todo=todo)  # 기존의 데이터를 같이 가져와서 edit.html에서 보여줌

# update 처리 로직
# update하는 경로를 라우트에 추가한다.
# 변경한 데이터를 가져와서 db에 작성
# @app.route('/todos/<int:id>/update', methods=["POST"])
# def update(id):
#     todo = Todo.query.get(id)  # 기존의 데이터를 먼저 가져온다
#     todo.todo = request.form['todo']  # 사용자가 입력한 todo 항목을 todo.todo로 바꿈
#     todo.deadline = request.form['deadline']  # 사용자가 입력한 deadline 항목을 todo.deadline으로 바꿈
#     db.session.commit()
#     return redirect('/')


# /todos/3/upgrade = GET, 수정 버튼 누르기 = POST
@app.route('/todos/<int:id>/upgrade', methods=["POST", "GET"])   # url은 같은 이름을 가질 수 없으나, methods가 다르면 다른 이름으로 인식한다
def upgrade(id):
    todo = Todo.query.get(id)
    
    if request.method == "POST":
        # 게시물을 실제로 업데이트 하는 로직
        todo.todo = request.form['todo']   # 사용자가 입력한 정보를 todo.todo에 덮어씌움
        todo.deadline = request.form['deadline']
        
        # 실제로 DB 반영
        db.session.commit()
        
        # 어디로 보낼지 설정
        return redirect('/')
    
    # 수정할 수 있는 폼을 리턴 - get 방식
    return render_template('edit.html', todo=todo)






