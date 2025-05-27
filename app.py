from flask import Flask,render_template,redirect,request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
Scss(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

class My_Task(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String(100),nullable = False)
    complete = db.Column(db.Integer,default = 0)
    created = db.Column(db.DateTime,default = datetime.utcnow)
    def __repr__(self)-> str:
        return f"Task{self.id}"

with app.app_context():
    db.create_all()
@app.route("/",methods=['POST','GET'])
def index():
    if request.method == 'POST':
        current_task = request.form.get('content')
        new_task = My_Task(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f'Error{e}'
    else:
        tasks = My_Task.query.order_by(My_Task.created).all()
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delet(id:int):
    tasks_delete = My_Task.query.get_or_404(id)
    try:
        db.session.delete(tasks_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f'Error:{e}'

@app.route('/edit/<int:id>',methods=["POST","GET"])
def edit(id:int):
    task = My_Task.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f'Error:{e}'
    else:
        return render_template('edit.html',task=task)







if __name__ == "__main__":
    app.run(debug=True)