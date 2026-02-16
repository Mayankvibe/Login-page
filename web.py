from flask import Flask,request,render_template,redirect,flash
from flask_sqlalchemy import SQLAlchemy

web=Flask(__name__)
web.secret_key="found_key"

web.config['SQLALCHEMY_DATABASE_URI']='sqlite:///try.db'
web.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(web)

class user(db.Model):
    id=db.Column('id',db.Integer,primary_key=True)
    name=db.Column('name',db.String(30),nullable=False)
    email=db.Column('email',db.String(30),nullable=False)
    contact=db.Column('contact',db.String(13))
@web.route('/')
def home():
    return render_template("index.html")
@web.route('/login',methods=['POST','GET'])
def login():
    if request.method=='GET':
        return render_template('base.html')
       
    else:
        db.create_all()
        name=request.form.get('name')
        email=request.form.get('email')
        contact=request.form.get('contact')
        new_user=user(name=name,email=email,contact=contact)
        db.session.add(new_user)
        db.session.commit()
        flash('Login Successfully ! Welcome Back')
        return redirect('/')




if __name__=="__main__":
    web.run(debug=True)