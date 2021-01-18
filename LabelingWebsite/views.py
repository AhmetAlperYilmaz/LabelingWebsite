from flask import render_template, url_for, flash, redirect, request
from LabelingWebsite import app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
import psycopg2 as dbapi2
from Settings import db_name, db_user, db_pass, HOST, PORT, DB_PORT
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from passlib.hash import pbkdf2_sha256 as hasher
from database import Database, USERS

db = Database()

lm = LoginManager(app)
lm.login_view = 'login'

@lm.user_loader
def load_user(the_user):
    return db.get_user(the_user)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=64)])
    remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[Length(max=64)])
    surname = StringField('Surname', validators=[Length(max=64)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=64)])
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=64)])

@app.route('/')
def index():
    return render_template('index.html', title='Home Page')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = db.get_user(str(form.username.data))
        if user is not None:
            the_password = user.password
            if hasher.verify(str(form.password.data), the_password):
                login_user(user, remember = form.remember.data)
                flash(f'Login is successful. Welcome {form.username.data}', 'success')
                return render_template('index.html', title='Home Page')
            else:
                flash('Failed to login, please try again','danger')
    return render_template('login.html', title='Login', form = form)

@login_required
@app.route("/logout")
def logout():
    if not current_user.is_authenticated:
        flash('You have not logged in. You cannot log out', 'danger')
        return redirect("/")
    else:
        logout_user()
        flash('You have successfully logged out.', 'success')
        return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    hash_password = hasher.hash(str(form.password.data))
    if form.validate_on_submit():
        user = db.get_user(str(form.username.data))
        email = db.get_email(str(form.email.data))
        if user is None and email is None:
            result = db.add_user(str(form.username.data), hash_password)
            result_2 = db.add_user_info(str(form.email.data),str(form.username.data),str(form.name.data),str(form.surname.data))
            result_3 = db.add_user_stats(str(form.username.data))
            if result == "success" and result_2 == "success":
                flash(f'Account is successfully created for the username: {form.username.data}','success')
                return redirect(url_for('login'))
            else:
                flash(f'Failed to register your account please try again.', 'danger')
        elif user is not None:
            flash(f'Username is already taken. Please change it.', 'danger')
            return render_template('signup.html', title='Register', form = form)
        elif email is not None:
            flash(f'Email is already taken. Please change it.', 'danger')
            return render_template('signup.html', title='Register', form = form)
    return render_template('signup.html', title='Register', form = form)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile Page')

@app.route('/del')
def deleting_db():
    with dbapi2.connect(database=db_name, user=db_user, password=db_pass, host=HOST, port=DB_PORT) as conn:
        with conn.cursor() as cursor:
            query = """DROP TABLE IF EXISTS USERS, USER_INFO, USER_STATS CASCADE"""
            cursor.execute(query)
            conn.commit()

    return redirect(url_for('index'))

@app.route('/ini')
def initializing_db():
    with dbapi2.connect(database=db_name, user=db_user, password=db_pass, host=HOST, port=DB_PORT) as conn:
        with conn.cursor() as cursor:
            query = """CREATE TABLE USERS
                    (
                        USERNAME character varying(64) NOT NULL,
                        PASSWORD character varying(255) NOT NULL,
                        PRIMARY KEY (USERNAME),
                        UNIQUE (USERNAME)
                    );"""
            cursor.execute(query)
            query = """CREATE TABLE USER_INFO
                    (
	                    EMAIL character varying(64) NOT NULL,
                        USERNAME character varying(64) NOT NULL,
	                    NAME character varying(64) DEFAULT NULL,
	                    SURNAME character varying(64) DEFAULT NULL,
                        PRIMARY KEY (EMAIL),
                        UNIQUE (EMAIL),
                        CONSTRAINT USERNAME
	                    FOREIGN KEY (USERNAME)
                        REFERENCES USERS(USERNAME) ON DELETE CASCADE
                    );"""
            cursor.execute(query)
            query = """CREATE TABLE USER_STATS
                    (
                        USERNAME character varying(64) NOT NULL,
	                    UPLOADED_COUNT INTEGER,
                        LABELED_COUNT INTEGER,
	                    DOWNLOADED_COUNT INTEGER,
                        PRIMARY KEY (USERNAME),
	                    FOREIGN KEY (USERNAME)
                        REFERENCES USERS(USERNAME) ON DELETE CASCADE
                    );"""
            cursor.execute(query)
            conn.commit()

    return redirect(url_for('index'))