import psycopg2 as dbapi2
from Settings import db_name, db_user, db_pass, HOST, PORT, DB_PORT
from flask_login import UserMixin

class USERS(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.active = True
        self.is_admin = False
    
    def get_id(self):
        return self.username

    @property
    def is_active(self):
        return self.active

class USER_INFO:
    def __init__(self, username, email, name, surname):
        self.username = username
        self.email = email
        self.name = name
        self.surname = surname

class USER_STATS:
    def __init__(self, username, labeled_count, downloaded_count, uploaded_count):
        self.username = username
        self.labeled_count = labeled_count
        self.downloaded_count = downloaded_count
        self.uploaded_count= uploaded_count

class LABEL_CATEGORIES:
    def __init__(self, labeled_as, total_count, total_download):
        self.labeled_as = labeled_as
        self.total_count = total_count
        self.total_download = total_download

class IMAGES:
    def __init__(self, image_id, image_path, height, width, username):
        self.image_id = image_id
        self.image_path = image_path
        self.height = height
        self.width = width
        self.username = username

class IMAGE_STATS:
    def __init__(self, image_id, total_count_label, total_count_download, labeled_as):
        self.image_id = image_id
        self.total_count_label = total_count_label
        self.total_count_download = total_count_download
        self.labeled_as = labeled_as

class Database:
    def __init__(self):
        self.users = []
        self.images = []

    def add_user(self, username, password):
        try:
            with dbapi2.connect(database=db_name, user=db_user, password=db_pass, host=HOST, port=DB_PORT) as conn:
                with conn.cursor() as cursor:
                    statement = """INSERT INTO USERS (USERNAME, PASSWORD) VALUES (%s, %s)"""
                    cursor.execute(statement, (username, password))
            return "success"
        except Exception:
            return "fail"

    def add_user_info(self, email, username, name, surname):
        try:
            with dbapi2.connect(database=db_name, user=db_user, password=db_pass, host=HOST, port=DB_PORT) as conn:
                with conn.cursor() as cursor:
                    statement = """INSERT INTO USER_INFO (EMAIL, USERNAME, NAME, SURNAME) VALUES (%s, %s, %s, %s)"""
                    cursor.execute(statement, (email, username, name, surname))
            return "success"
        except Exception:
            return "fail"

    def add_user_stats(self, the_username):
        try:
            with dbapi2.connect(database=db_name, user=db_user, password=db_pass, host=HOST, port=DB_PORT) as conn:
                with conn.cursor() as cursor:
                    statement = """INSERT INTO USER_STATS (USERNAME, UPLOADED_COUNT, LABELED_COUNT, DOWNLOADED_COUNT) VALUES (%s, 0, 0, 0);"""
                    data = (the_username,)
                    cursor.execute(statement, data)
            return "success"
        except Exception:
            return "fail"

    def get_user(self, the_username):
        statement = """SELECT * FROM USERS WHERE USERNAME = '%s';""" % (the_username,)
        with dbapi2.connect(database=db_name, user=db_user, password=db_pass, host=HOST, port=DB_PORT) as conn:
            with conn.cursor() as cursor:
                cursor.execute(statement)
                user = cursor.fetchall()
                if user is not None:
                    for row in user:
                        user = USERS(row[0], row[1])
                        return user
                else:
                    return None

    def get_email(self, the_email):
        statement = """SELECT * FROM USER_INFO WHERE EMAIL = '%s';""" % (the_email,)
        with dbapi2.connect(database=db_name, user=db_user, password=db_pass, host=HOST, port=DB_PORT) as conn:
            with conn.cursor() as cursor:
                cursor.execute(statement)
                email = cursor.fetchall()
                if email is not None:
                    for row in email:
                        email = USER_INFO(row[0], row[1], row[2], row[3])
                        return email
                else:
                    return None
    
    def get_user_stats(self, the_username):
        statement = """SELECT * FROM USER_STATS WHERE USERNAME = '%s';""" % (the_username,)
        with dbapi2.connect(database=db_name, user=db_user, password=db_pass, host=HOST, port=DB_PORT) as conn:
            with conn.cursor() as cursor:
                cursor.execute(statement)
                user_stats = cursor.fetchall()
                if user_stats is not None:
                    for row in user_stats:
                        user_stats = USERS(row[0], row[1], row[2], row[3])
                        return user_stats
                else:
                    return None