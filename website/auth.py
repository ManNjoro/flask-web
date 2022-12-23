from flask import Blueprint,render_template,request,flash,redirect,url_for,Flask,session
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql.connector
from flask_login import login_user,login_required,logout_user,current_user

auth=Blueprint('auth',__name__)
app = Flask(__name__)
mysql = MySQL(app)
@auth.route('/login', methods=['GET','POST'])
def login():
    
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM sign_up WHERE email=%s',(email,))
        
        user = cur.fetchone()
        if user:
            session['loggedin']=True
            session['email']=user['email']
            if check_password_hash(user['passwd'], password):
                flash('Logged in successfully',category='success')
                loginuser = User(user)
                login_user(loginuser,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password,try again.',category='error')
        else:
            flash('Email does not exist.',category='error')
    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET','POST'])
def sign_up():
    app = Flask(__name__)
    mysql = MySQL(app)
    cur = mysql.connection.cursor()
    if request.method=='POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        cur.execute('SELECT * FROM sign_up WHERE email=%s',(email,))
        user = cur.fetchone()
        if user:
            flash('Email already exists.',category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(fname) <2:
            flash('First Name must be greater than 2 characters', category='error')
        elif len(lname) <2:
            flash('Last Name must be greater than 2 characters', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 8:
            flash('Password must be at least than 8 characters', category='error')
        else:
            # add user to db
            
            cur.execute("INSERT INTO sign_up (fname,lname,email,passwd) VALUES (%s, %s,%s,%s)",(fname,lname,email,generate_password_hash(password1,method='sha256')))
            # commit to db
            mysql.connection.commit()
            cur.close()
            flash('Account created', category='success')
            return redirect(url_for('auth.login'))
    return render_template("signup.html",user=current_user)

@auth.route('/bookings', methods=['GET','POST'])
@login_required
def bookings():
    if request.method=='POST':
        flash("Form submitted successfully!",category='success')
    return render_template("bookings.html",user=current_user)
