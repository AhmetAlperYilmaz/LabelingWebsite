"""
Routes and views for the flask application.
"""

from flask import render_template, url_for, flash, redirect
from LabelingWebsite import app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from passlib.hash import pbkdf2_sha256 as hasher
from Settings import PASSWORDS, ADMIN_USERS

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=64)])
    remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[Length(max=64)])
    surname = StringField('Surname', validators=[Length(max=64)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=64)])
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=1, max=64)])

@app.route('/')
def index():
    return render_template('index.html', title='Home Page')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        #hashed = hasher.verify(PASSWORDS['admin'])
        if form.username.data == 'admin' and form.password.data == "performance":
            flash('Login successful', 'success')
            return render_template('index.html', title='Home Page')
        else:
            flash('Failed to login, please try again','danger')
    return render_template('login.html', title='Login', form = form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        flash(f'Account successfully created for the username: {form.username.data}!','success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Register', form = form)