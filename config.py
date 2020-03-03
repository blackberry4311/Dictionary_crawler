"""Configuration for different environment.
flask app automatically read this file
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    TESTING = True
    HOST = "0.0.0.0"
    PORT = 1080
    UPLOAD_LOCATION = os.path.join(basedir, 'upload')
