"""
The flask application package.
"""

from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MySecretKey'
Bootstrap(app)

import LabelingWebsite.views
