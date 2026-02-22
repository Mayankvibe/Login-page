from flask import Flask,request,render_template,redirect,flash,Request
from flask_sqlalchemy import SQLAlchemy

web=Flask(__name__)
web.secret_key="found_key"

web.config['SQLALCHEMY_DATABASE_URI']='sqlite:///try.db'
web.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(web)

class user(db.Model):
    id=db.Column('id',db.Integer,primary_key=True)
    name=db.Column('name',db.String(30),nullable=False)
    email=db.Column('email',db.String(30),nullable=False,unique=True)
    contact=db.Column('contact',db.String(13))

    
@web.route('/')
def home():
    return render_template("index.html")

@web.route('/login',methods=['POST','GET'])
def login():
    if request.method=='GET':
        return render_template('base.html')
       
    else:
        name=request.form.get('name')
        email=request.form.get('email')
        contact=request.form.get('contact')
        new_user=user(name=name,email=email,contact=contact)
        db.session.add(new_user)
        db.session.commit()
        flash('Login Successfully ! Welcome Back')
        return redirect('/')

 # it fetch the data from database and show   
@web.route('/show')
def show():
    all_data=user.query.all()
    return render_template('users.html',users=all_data)

# we edit the data and store 
@web.route("/edit/<int:i>" , methods=["POST"])
def edit(i):
    u=user.query.get_or_404(i)
    return render_template("edit.html" ,edit_data=u )
@web.route('/update/<int:i>' , methods=["POST"])
def update(i):
        u=user.query.get_or_404(i)
        u.name=request.form.get('name')
        u.email=request.form.get('email')
        u.contact=request.form.get('contact')
        
        db.session.commit()
        
        return redirect("/show")
    
    

# to delete the data from database
@web.route('/delete/<int:i>', methods =['POST'])
def delete(i):
    u=user.query.get_or_404(i)
    db.session.delete(u)
    db.session.commit()
    return redirect('/show')

if __name__=="__main__":
    with web.app_context():
        db.create_all() #create the data table
        web.run(debug=True)