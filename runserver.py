"""
This script runs the LabelingWebsite application using a development server.
"""

from os import environ
from LabelingWebsite import app
from Settings import PORT, HOST, DEBUG

if __name__ == '__main__':
    app.run(HOST, PORT, debug = DEBUG)
