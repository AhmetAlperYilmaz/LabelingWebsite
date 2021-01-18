from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
# key = "Calvin"
# hashed_key = hasher.hash(password)
# hashed_key '$pbkdf2-sha256$29000$eu8dw3jvnVOK8T5n7F0LQQ$yQetZHaNhOnEa66n/2CHcoGXzOskzB76..OtPEVZiKA'
# verify_key = hasher.verify("Calvin", hashed_key)
# verify_key is True
app.config['SECRET_KEY'] = '$pbkdf2-sha256$29000$eu8dw3jvnVOK8T5n7F0LQQ$yQetZHaNhOnEa66n/2CHcoGXzOskzB76..OtPEVZiKA'
Bootstrap(app)

import LabelingWebsite.views