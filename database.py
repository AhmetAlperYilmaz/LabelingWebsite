import psycopg2 as dbapi2
from Settings import db_name, db_user, db_pass, HOST, PORT, DB_PORT
from flask_login import UserMixin
import os

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
    def __init__(self, email, username, name, surname):
        self.username = username
        self.email = email
        self.name = name
        self.surname = surname

class USER_STATS:
    def __init__(self, username, uploaded_count, labeled_count, downloaded_count):
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
    def __init__(self, image_id, height, width, username):
        self.image_id = image_id
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
        self.last_image_id = 0

    def add_user(self, username, password):
        try:
            url = os.getenv("DATABASE_URL")
            with dbapi2.connect(url) as conn:
                with conn.cursor() as cursor:
                    statement = """INSERT INTO USERS (USERNAME, PASSWORD) VALUES (%s, %s)"""
                    cursor.execute(statement, (username, password))
            return "success"
        except Exception:
            return "fail"

    def add_user_info(self, email, username, name, surname):
        try:
            url = os.getenv("DATABASE_URL")
            with dbapi2.connect(url) as conn:
                with conn.cursor() as cursor:
                    statement = """INSERT INTO USER_INFO (EMAIL, USERNAME, NAME, SURNAME) VALUES (%s, %s, %s, %s)"""
                    cursor.execute(statement, (email, username, name, surname))
            return "success"
        except Exception:
            return "fail"

    def add_user_stats(self, the_username):
        try:
            url = os.getenv("DATABASE_URL")
            with dbapi2.connect(url) as conn:
                with conn.cursor() as cursor:
                    statement = """INSERT INTO USER_STATS (USERNAME, UPLOADED_COUNT, LABELED_COUNT, DOWNLOADED_COUNT) VALUES (%s, 0, 0, 0);"""
                    data = (the_username,)
                    cursor.execute(statement, data)
            return "success"
        except Exception:
            return "fail"
    
    def add_label_category(self, labeled_as):
        try:
            url = os.getenv("DATABASE_URL")
            with dbapi2.connect(url) as conn:
                with conn.cursor() as cursor:
                    statement = """INSERT INTO LABEL_CATEGORIES (LABELED_AS, TOTAL_COUNT, TOTAL_DOWNLOAD) VALUES (%s, 0, 0);"""
                    data = (labeled_as,)
                    cursor.execute(statement, data)
            return "success"
        except Exception:
            return "fail"

    def add_image(self, image_id, height, width, username):
        try:
            url = os.getenv("DATABASE_URL")
            with dbapi2.connect(url) as conn:
                with conn.cursor() as cursor:
                    statement = """INSERT INTO IMAGES (IMAGE_ID, HEIGHT, WIDTH, USERNAME) VALUES (%d, %s, %s, %s)"""
                    data = (image_id, height, width, username)
                    cursor.execute(statement, data)
            return "success"
        except Exception:
            return "fail"

    def add_image_stats(self, image_id, total_count_label, total_count_download, labeled_as):
        try:
            url = os.getenv("DATABASE_URL")
            with dbapi2.connect(url) as conn:
                with conn.cursor() as cursor:
                    statement = """INSERT INTO IMAGE_STATS (IMAGE_ID, TOTAL_COUNT_LABEL, TOTAL_COUNT_DOWNLOAD, LABELED_AS) VALUES (%d, 0, 0, %s)"""
                    data = (image_id, labeled_as)
                    cursor.execute(statement, data)
            return "success"
        except Exception:
            return "fail"

    def get_user(self, the_username):
        statement = """SELECT * FROM USERS WHERE USERNAME = '%s';""" % (the_username,)
        url = os.getenv("DATABASE_URL")
        with dbapi2.connect(url) as conn:
            with conn.cursor() as cursor:
                cursor.execute(statement)
                user = cursor.fetchall()
                if user is not None:
                    for row in user:
                        user = USERS(row[0], row[1])
                        return user
                else:
                    return None

    def get_user_info(self, the_username):
        statement = """SELECT * FROM USER_INFO WHERE USERNAME = '%s';""" % (the_username,)
        url = os.getenv("DATABASE_URL")
        with dbapi2.connect(url) as conn:
            with conn.cursor() as cursor:
                cursor.execute(statement)
                user_info = cursor.fetchall()
                if user_info is not None:
                    for row in user_info:
                        user_info = USER_INFO(row[0], row[1], row[2], row[3])
                        return user_info
                else:
                    return None

    def get_email(self, the_email):
        url = os.getenv("DATABASE_URL")
        statement = """SELECT * FROM USER_INFO WHERE EMAIL = '%s';""" % (the_email,)
        with dbapi2.connect(url) as conn:
            with conn.cursor() as cursor:
                cursor.execute(statement)
                user_info = cursor.fetchall()
                if user_info is not None:
                    for row in user_info:
                        user_info = USER_INFO(row[0], row[1], row[2], row[3])
                        return user_info
                else:
                    return None
    
    def get_user_stats(self, the_username):
        statement = """SELECT * FROM USER_STATS WHERE USERNAME = '%s';""" % (the_username,)
        url = os.getenv("DATABASE_URL")
        with dbapi2.connect(url) as conn:
            with conn.cursor() as cursor:
                cursor.execute(statement)
                user_stats = cursor.fetchall()
                if user_stats is not None:
                    for row in user_stats:
                        user_stats = USER_STATS(row[0], row[1], row[2], row[3])
                        return user_stats
                else:
                    return None
    
    def get_image(self, image_id):
        statement = """SELECT * FROM IMAGES WHERE IMAGE_ID = '%d';""" % (image_id,)
        url = os.getenv("DATABASE_URL")
        with dbapi2.connect(url) as conn:
            with conn.cursor() as cursor:
                cursor.execute(statement)
                images = cursor.fetchall()
                if images is not None:
                    for row in images:
                        images = IMAGES(row[0], row[1], row[2], row[3])
                        return images
                else:
                    return None

    def get_label_category(self, labeled_as):
        url = os.getenv("DATABASE_URL")
        statement = """SELECT * FROM LABEL_CATEGORIES WHERE LABELED_AS = '%s';""" % (labeled_as,)
        with dbapi2.connect(url) as conn:
            with conn.cursor() as cursor:
                cursor.execute(statement)
                category = cursor.fetchall()
                if category is not None:
                    for row in category:
                        category = LABEL_CATEGORIES(row[0], row[1], row[2])
                        return category
                else:
                    return None

    def get_image_stats(self, image_id):
        statement = """SELECT * FROM IMAGE_STATS WHERE IMAGE_ID = '%d';""" % (image_id,)
        url = os.getenv("DATABASE_URL")
        with dbapi2.connect(url) as conn:
            with conn.cursor() as cursor:
                cursor.execute(statement)
                image_stats = cursor.fetchall()
                if image_stats is not None:
                    for row in image_stats:
                        image_stats = IMAGE_STATS(row[0], row[1], row[2], row[3])
                        return image_stats
                else:
                    return None