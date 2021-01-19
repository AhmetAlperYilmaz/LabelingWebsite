"""
This script runs the LabelingWebsite application using a development server.
"""
import os
from os import environ
from LabelingWebsite import app
from Settings import PORT, HOST, DEBUG
from dbinit import initialize

HEROKU = True

if(not HEROKU):
    os.environ['DATABASE_URL'] =  "dbname='LabelingDB' user='postgres' host='localhost' password='KingHarlaus26 port='5432'"
    initialize(os.environ.get('DATABASE_URL'))

if __name__ == '__main__':
    if(not HEROKU):
        app.run(HOST, PORT, debug = DEBUG)
    else:
        app.run()
