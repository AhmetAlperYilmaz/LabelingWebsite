from flask import render_template, url_for, flash, redirect, request, jsonify, make_response
from LabelingWebsite import app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
import psycopg2 as dbapi2
from Settings import db_name, db_user, db_pass, HOST, PORT, DB_PORT
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from passlib.hash import pbkdf2_sha256 as hasher
from database import Database, USERS
from psycopg2 import extensions
import os
from werkzeug.utils import secure_filename

extensions.register_type(extensions.UNICODE)
extensions.register_type(extensions.UNICODEARRAY)

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
    #“Remember Me” prevents the user from accidentally being logged out when they close their browser. 
    #This does NOT mean remembering or pre-filling the user’s username or password in a login form after the user has logged out.

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[Length(max=64)])
    surname = StringField('Surname', validators=[Length(max=64)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=64)])
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=64)])

class ImageForm(FlaskForm):
    height = StringField('Enter the image height', validators=[Length(max=4)])
    width = StringField('Enter the image width', validators=[Length(max=4)])
    label = StringField('Enter the image label (optional)', validators=[Length(max=255)])

class UpdateForm(FlaskForm):
    oldpassword = PasswordField('Old Password', validators=[InputRequired(), Length(min=8, max=64)])
    newpassword = PasswordField('New Password', validators=[InputRequired(), Length(min=8, max=64)])
    confirm = PasswordField('Confirm New Password', validators=[InputRequired(), Length(min=8, max=64)])

class UpdateInfo(FlaskForm):
    name = StringField('New Name', validators=[Length(max=64)])
    surname = StringField('New Surname', validators=[Length(max=64)])
    username = StringField('New Username', validators=[InputRequired(), Length(min=1, max=64)])
    email = StringField('New Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=64)])
    confirm = PasswordField('Confirm Your Changes with Password', validators=[InputRequired(), Length(min=8, max=64)])

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
                if(form.remember.data):
                    login_user(user, remember = True)
                else:
                    login_user(user, remember = False)
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
    a_user_info = db.get_user_info(current_user.username)
    a_user_stats = db.get_user_stats(current_user.username)
    return render_template('profile.html', title='Profile Page', your_info=a_user_info, your_stats=a_user_stats)

@login_required
@app.route("/update-password", methods=['GET','POST'])
def update_profile():
    if not current_user.is_authenticated:
        return redirect("/")
    update = UpdateForm()
    if update.validate_on_submit():
        if str(update.newpassword.data) != str(update.confirm.data):
            flash(f"New passwords don't match. Try again.",'danger')
            return redirect("/update-password")
        user = db.get_user(current_user.username)
        if hasher.verify(str(update.oldpassword.data), user.password):
            new = hasher.hash(str(update.newpassword.data))
            statement = """UPDATE USERS SET PASSWORD = '%s' WHERE USERNAME = '%s'""" % (new, current_user.username)
            url = os.getenv("DATABASE_URL")
            with dbapi2.connect(url) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(statement)
                    connection.commit()
                    flash(f"Your password has changed successfully.",'success')
                    logout_user()
                    return redirect("/login")
        else:
            flash(f"The old password you entered is incorrect. Try again.",'danger')
            return redirect("/update-password")
    return render_template("update-password.html", title = "Change Password", update = update)

@app.route('/update-info', methods=['GET', 'POST'])
@login_required
def update_info():
    if not current_user.is_authenticated:
        return redirect("/")
    update = UpdateInfo()
    if update.validate_on_submit():
        user_info_by_email = db.get_email(str(update.email.data))
        if user_info_by_email is not None:
            flash(f"This email is already taken. Please try another email.",'danger')
            return redirect("/update-info")
        user = db.get_user(str(update.username.data))
        if user is not None:
            flash(f"This username is already taken. Please try another username.",'danger')
            return redirect("/update-info")
        user_info = db.get_user_info(current_user.username)
        user_2 = db.get_user(current_user.username)
        if(hasher.verify(str(update.confirm.data), user_2.password)):
            url = os.getenv("DATABASE_URL")
            with dbapi2.connect(url) as connection:
                with connection.cursor() as cursor:
                    statement = """UPDATE USER_INFO SET NAME = '%s' WHERE EMAIL = '%s'""" % (str(update.name.data), user_info.email)
                    cursor.execute(statement)
                    statement = """UPDATE USER_INFO SET SURNAME = '%s' WHERE EMAIL = '%s'""" % (str(update.surname.data), user_info.email)
                    cursor.execute(statement)
                    statement = """UPDATE USERS SET USERNAME = '%s' WHERE USERNAME = '%s'""" % (str(update.username.data), user_2.username)
                    cursor.execute(statement)
                    statement = """UPDATE USER_INFO SET EMAIL = '%s' WHERE EMAIL = '%s'""" % (str(update.email.data), user_info.email)
                    cursor.execute(statement)
                    connection.commit()
                    flash(f"Your info has changed successfully.",'success')#done
                    return redirect("/profile")  
        else:
            flash(f"The password you entered is incorrect. Try again.",'danger')
            return redirect("/update-info")
    return render_template("update-info.html", title = "Update Info", update = update)

app.config["IMAGE_UPLOADS"] = "C://Users//alper//Desktop//VStudioDatabase//LabelingWebsite//LabelingWebsite//static//img//uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG","JPG","JPEG","GIF"]

def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@login_required
@app.route('/label', methods=['GET', 'POST'])
def label():
    if request.method == "POST":  
        if request.files:
            image = request.files["image"]
            if image.filename == "":
                flash(f'Image must have a filename', 'danger')
                return redirect(request.url)
            if not allowed_image(image.filename):
                flash(f'Image extension is not allowed', 'danger')
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            flash(f'Image has been saved', 'success')
            return redirect(request.url)

    return render_template('label.html', title='Label Page')

@app.route('/del')
def deleting_db():
    url = os.getenv("DATABASE_URL")
    with dbapi2.connect(url) as conn:
        with conn.cursor() as cursor:
            query = """DROP TABLE IF EXISTS USERS, USER_INFO, USER_STATS, LABEL_CATEGORIES, IMAGES, IMAGE_STATS CASCADE"""
            cursor.execute(query)
            conn.commit()

    return redirect(url_for('index'))

@app.route('/ini')
def initializing_db():
    url = os.getenv("DATABASE_URL")
    with dbapi2.connect(url) as conn:
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
	                    FOREIGN KEY (USERNAME)
                        REFERENCES USERS(USERNAME) ON UPDATE CASCADE ON DELETE CASCADE
                    );"""
            cursor.execute(query)
            query = """CREATE TABLE USER_STATS
                    (
                        USERNAME character varying(64) NOT NULL,
	                    UPLOADED_COUNT INTEGER DEFAULT 0,
                        LABELED_COUNT INTEGER DEFAULT 0,
	                    DOWNLOADED_COUNT INTEGER DEFAULT 0,
                        PRIMARY KEY (USERNAME),
	                    FOREIGN KEY (USERNAME)
                        REFERENCES USERS(USERNAME)  ON UPDATE CASCADE ON DELETE CASCADE
                    );"""
            cursor.execute(query)
            query = """CREATE TABLE LABEL_CATEGORIES
                    (
                        LABELED_AS character varying(255) NOT NULL,
	                    TOTAL_COUNT INTEGER,
                        TOTAL_DOWNLOAD INTEGER,
                        PRIMARY KEY (LABELED_AS),
                        UNIQUE(LABELED_AS)
                    );"""
            cursor.execute(query)
            query = """CREATE TABLE IMAGES
                    (
                        IMAGE_ID INTEGER NOT NULL,
                        HEIGHT INT NOT NULL,
	                    WIDTH INT NOT NULL,
                        USERNAME character varying(64) NOT NULL,
                        PRIMARY KEY (IMAGE_ID),
                        UNIQUE (IMAGE_ID),
	                    FOREIGN KEY (USERNAME)
                        REFERENCES USERS(USERNAME) ON DELETE CASCADE
                    );"""
            cursor.execute(query)
            query = """CREATE TABLE IMAGE_STATS
                    (
                        IMAGE_ID INTEGER NOT NULL,
	                    TOTAL_COUNT_LABEL INTEGER DEFAULT 0,
                        TOTAL_COUNT_DOWNLOAD INTEGER DEFAULT 0,
                        LABELED_AS character varying(255) NOT NULL,
                        PRIMARY KEY (IMAGE_ID),
	                    FOREIGN KEY (IMAGE_ID)
                        REFERENCES IMAGES(IMAGE_ID) ON DELETE CASCADE,
                        FOREIGN KEY (LABELED_AS)
                        REFERENCES LABEL_CATEGORIES(LABELED_AS) ON DELETE CASCADE
                    );"""
            cursor.execute(query)
            
            conn.commit()

    return redirect(url_for('index'))