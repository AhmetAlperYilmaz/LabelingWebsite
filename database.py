import psycopg2 as dbapi2

class user:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class user_information:
    def __init__(self, username, email, name, surname):
        self.username = username
        self.email = email
        self.name = name
        self.surname = surname

class user_stats:
    def __init__(self, username, labeled_count, downloaded_count, uploaded_count):
        self.username = username
        self.labeled_count = labeled_count
        self.downloaded_count = downloaded_count
        self.uploaded_count= uploaded_count

class Database:
    def __init__(self):
        self.users = {}
        self.images = {}