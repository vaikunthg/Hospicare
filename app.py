from datetime import datetime
from flask import Flask, json,render_template,redirect,session
from flask.globals import request, session
from flask.helpers import url_for
from flask_login.mixins import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.elements import Null
from verification import sendMail,sendPhoneOtp
from flask_login import login_manager


app = Flask(__name__)
# use ENV asa 'dev' or 'demo'
# use 'demo'  to try the demo of the software where email and password must be entered same
# in 'demo' mode use Ur Name Instead of your number during registration
ENV = 'demo'

if (ENV == 'dev'):
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres:2729@localhost/test'

else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SECRET_KEY'] = b'secretism'
db = SQLAlchemy(app)

login_manager = login_manager.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# database models
class registration(UserMixin, db.Model):
    __tablename__= 'registration'
    uuid = db.Column(db.Integer(),primary_key=True)
    number = db.Column(db.String(),unique=True,nullable=False)
    password = db.Column(db.String(),nullable=False)
    accountType = db.Column(db.String(),unique=True,nullable=False)
    def __init__(self,number,password,accountType):
        self.number=number
        self.password=password
        self.accountType=accountType



class patients(db.Model):
    __tablename__= 'patients'
    uuid = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(),nullable=False)
    Age = db.Column(db.Integer(),nullable=False)
    gender = db.Column(db.String(),nullable=False)
    dob = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    email = db.Column(db.String(),unique=True,nullable=False)

    def __init__(self,name,Age,gender,dob,email):
        self.name = name
        self.Age = Age
        self.gender = gender
        self.dob = dob
        self.email = email
    
class staff(db.Model):
    __tablename__= 'staff'
    uuid = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(),nullable=False)
    address = db.Column(db.String(),nullable=False)
    hospital = db.Column(db.String(),nullable=False)
    department = db.Column(db.String(),nullable=False)
    contactNo = db.Column(db.String(),unique=True,nullable=False)
    post = db.Column(db.String(),nullable=False)
    gender = db.Column(db.String(),nullable=False)
    dob = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    Age = db.Column(db.Integer(),nullable=False)

    def __init__(self,name,address,hospital,contactNo,post,gender,dob,Age):
        self.name = name
        self.address = address
        self.hospital = hospital
        self.contactNo = contactNo
        self.post = post
        self.gender = gender
        self.dob = dob
        self.Age = Age


class bloodBank(db.Model):
    __tablename__= 'bloodbank'
    uuid = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(),nullable=False)
    # under hospital or private
    ownership = db.Column(db.String(),nullable=False)
    address = db.Column(db.String(),nullable=False)
    contactNo = db.Column(db.String(),unique=True,nullable=False)
    def __init__(self,name,ownership,address,contactNo):
        self.name = name
        self.address = address
        self.ownership = ownership
        self.contactNo = contactNo

class admin(db.Model):
    __tablename__= 'admin'
    uuid = db.Column(db.Integer(),primary_key=True)
    email = db.Column(db.String(),unique=True,nullable=False)
    password = db.Column(db.String(),nullable=False)
    def __init__(self,email,password):
        self.email = email
        self.password = password
    
#global Variables and variables
global phoneNo,phoneotp,status,name,role,email
name=""
phoneNo = ""
role =  ""
phoneotp = ""
email = ""


# methods
@login_manager.user_loader
def load_user(user_id):
    return db.Query.get(int(user_id))
# methods end



@app.route('/home')
@app.route('/<user>/')
@app.route('/<user>/<role>/')
@app.route('/')
def home(user="",role=""):
    global name
    name = user
    if(name!=""):
        return render_template('index.html',user=user)
    elif(name!="" and role!=""):
        return render_template('index.html',user=name,role="admin".replace('"',""))
    return render_template('index.html',user="")

@app.route('/bloodbank')
def bloodbank():
    demo = [{'id':1,'name':'Lokmanya blood Bank','address':'Pune','phone':'90750xxxxx'},
            {'id':2,'name':'MMF Ratna blood Bank','address':'Pune','phone':'91735xxxxx'},
            {'id':3,'name':'Joglekar blood Bank','address':'Pune','phone':'83235xxxxx'},
            {'id':4,'name':'Swanand blood Bank','address':'Pune','phone':'21335xxxxx'},
            {'id':5,'name':'Navjeenvan Blood Bank','address':'Pune','phone':'55223xxxxx'}]
    return render_template('bloodbank.html', user=name, items=demo)

@app.route('/hospitals')
def hospitals():
    
    return render_template('hospital.html', user=name)

@app.route('/status')
def status():
    return render_template('status.html')

@app.route('/emergency',methods = ['GET', 'POST'])
def emergency():
    return render_template('emergency.html', user=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global name
    if(ENV=="dev"):
        if request.method == "POST":
            userid = str(request.form.get("userid"))
            password = str(request.form.get("password"))
            query = db.Query(registration).filter(registration.number==userid, registration.password==password).first()
            if(query):
                name = db.Query(patients).get(patients.uuid==query.uuid)
                session['user'] = name
                session['logged_in'] = True
                session['role'] = ""
                return render_template('login.html', user=name,error="")    
            else:
                return render_template('login.html',error="Invalid Username Or Password")
    elif(ENV=='demo'):
        if(request.method == "POST"):
            name = str(request.form.get("userid"))
            password = str(request.form.get("password"))
            if(name==password):
                session['user'] = name
                session['logged_in'] = True
                session['role'] = ""
                return redirect(url_for('home',user=name,role=session['role'].replace('"',"")))
    return render_template('login.html', user=name,error="")
    

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    global phoneNo
    if(ENV=="dev"):
        if request.method == "POST":
            phoneNo = str(request.form.get("userid"))
            password = str(request.form.get("password"))
            if(db.session.query(registration).filter(registration.number==phoneNo and registration.password==password).count()==0):
                return redirect(url_for('completeRegistration'))
            else:
                return render_template('signin.html',error="Already Registered")
        
    elif(ENV=='demo'):
        if(request.method == "POST"):
            phoneNo = str(request.form.get("userid"))
            password = str(request.form.get("password"))
            return redirect(url_for('completeRegistration'))
    return render_template('signin.html', user=name)
    

@app.route('/complete-registration', methods=['GET', 'POST'])
def completeRegistration():
    global name,email
    if(ENV=='dev'):
        if request.method == "POST":
            name = str(request.form.get("name"))
            email = str(request.form.get("email"))
            password = str(request.form.get("password"))
            conPassword = str(request.form.get("confirm-password"))
            age = str(request.form.get("age"))
            dob = str(request.form.get("dob"))
            gender = str(request.form.get("gender"))
            if(password!=conPassword):
                return redirect(url_for('completeRegistration',password="Password Didnt Match"))
            regis = registration(phoneNo,password,"patient")
            patient = patients(name,age,gender,dob,email)
            db.session.add(regis)
            db.session.add(patient)
            db.session.commit()
            return redirect(url_for('verification'))

    elif(ENV=='demo'):
        if request.method == "POST":
            name = str(request.form.get("name"))
            email = str(request.form.get("email"))
            password = str(request.form.get("password"))
            conPassword = str(request.form.get("confirm-password"))
            age = str(request.form.get("age"))
            dob = str(request.form.get("dob"))
            gender = str(request.form.get("gender"))
            if(password!=conPassword):
                return redirect(url_for('completeRegistration',password="Password Didnt Match"))
            session['user'] = name
            session['role'] = ""
            return redirect(url_for('verification'))
    return render_template('complete-registration.html', user=name)

@app.route('/verification', methods=['GET', 'POST'])
def verification():
    global name,phoneNo,email
    if request.method == "POST":
        phoneotp = str(request.form.get("phoneOtp"))   
        phoneSentOtp = sendPhoneOtp(phoneNo)
        mailotp = str(request.form.get("mailOtp"))  
        mailSentOtp = sendMail(email)
        if(phoneotp==phoneSentOtp):
            if(mailotp==mailSentOtp):
                return redirect(url_for('home',user=session['user'].replace('"',""),role=session['role'].replace('"',"")))
        else:
            return redirect(url_for('verification.html',error="Invalid OTP entered"))
    return render_template('verification.html' , user=name)


@app.route('/userDetails')
def userDetails():
    return render_template('details.html',name="Sourav",gender="Male",dateofbirth="22/09/2002",emailId="souravkxx@gmail.com",phoneNo="999007xxxx",other="No Allergies")

@app.route('/about')
@app.route('/callUs')
def callUs(): 
    return render_template('callUs.html', user=name)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global name
    if(ENV=='dev'):
        userid = str(request.form.get("userid"))
        password = str(request.form.get("password"))
        query = db.Query(admin).filter(admin.email==userid, admin.password==password).first()
        if(query):
            name = db.Query(admin).get(admin.uuid==query.uuid)
            session['user'] = name
            session['logged_in'] = True
            session['role'] = "admin"
            return redirect(url_for('home',user=name,role=session['role'].replace('"',"")))
        return render_template('admin.html', user=name)
    elif(ENV=='demo'):
        if request.method == "POST":
            userid = str(request.form.get("userid"))
            password = str(request.form.get("password"))
            if(userid==password):
                print('in')
                session['user'] = name
                session['logged_in'] = True
                session['role'] = "admin"
                return redirect(url_for('home',user=name,role=session['role'].replace('"',"")))
            else:
                return render_template('admin.html',user="")
    return render_template('admin.html',user="")


@app.route('/forgotPass', methods=['GET', 'POST'])
def forgotPass():
    return render_template('forgot.html', user="")

if __name__ == '__main__':
    app.run(debug=True)
