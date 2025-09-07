from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):   
    sno = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime,default = datetime.utcnow)

    def __repr__(self)->str:
        return f"{self.sno} - {self.title}"

@app.route('/update/<int:sno>',methods= ['Get','POST'])
def update(sno):
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo  = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        # db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo  = Todo.query.filter_by(sno=sno).first()
    date_created = db.Column(db.DateTime,default = datetime.utcnow)

    return render_template('update.html',todo=todo)

    
    
    
    
@app.route('/delete/<int:sno>')
def delete(sno):
    todo  = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

with app.app_context():
    db.create_all()

@app.route("/",methods= ['Get','POST'])
def hello_world():
    if request.method =="POST":
        # print("post")
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    # print(allTodo)
    return render_template("index.html",allTodo=allTodo)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Use Render's port
    app.run(host="0.0.0.0", port=port, debug=True)  # debug=True optional for local
