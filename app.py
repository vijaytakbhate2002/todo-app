from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

title_size = 200
desc_size = 500
        
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(title_size),nullable = False)
    desc = db.Column(db.String(desc_size),nullable = False)
    time = db.Column(db.DateTime,default= datetime.utcnow)  

    def __repr__(self):
        return f"{self.sno} - {self.title}"

@app.before_first_request
def create_table():
    db.create_all()

@app.route("/",methods=["GET","POST"])
def index():
    with open("todo_completed.txt","r") as f:
        todo_completed_lis = f.readlines()
    if request.method == "POST":
        if len(request.form['title']) != 0:
            todo = Todo(title=request.form['title'],desc=request.form['desc'])
            db.session.add(todo)
            db.session.commit()
        request.method = "None"
    allTodos = Todo.query.all()
    return render_template("index.html",allTodo=allTodos,todo_completed_lis = todo_completed_lis)

@app.route("/Delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/Done/<int:sno>")
def done(sno):
    todo_completed = Todo.query.filter_by(sno=sno).first()
    todo_completed_str = str(todo_completed).split("-")[1]
    with open("todo_completed.txt","a") as f:
        f.write(todo_completed_str+"\n")
        db.session.delete(todo_completed)
        db.session.commit()
    with open("todo_completed.txt","r") as f:
        global todo_completed_lis
        todo_completed_lis = f.readlines()
    return redirect("/")

@app.route("/clear_done")
def clear_done():
    with open("todo_completed.txt","w") as f:
        f.write("") 
    return redirect("/") 

@app.route("/Update/<int:sno>",methods=['GET','POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    return render_template("update.html",todo=todo)
    
if __name__ == "__main__":
    app.run(debug=True, port = 8000)

