#coding=utf-8
'''
Created on 2016年12月27日

@author: huangning
'''
from flask import Flask, redirect, url_for
from flask_bcrypt import Bcrypt
from models import db
from main import main
from auth import auth
from ext_bcrypt import bcrypt

def create_app(object_name):
    """Create the app instance via `Factory Method`"""

    app = Flask(__name__)
    # Set the app config 
    app.config.from_object(object_name)

    # Will be load the SQLALCHEMY_DATABASE_URL from config.py to db object
    db.init_app(app)
    bcrypt.init_app(app)
    '''@app.route('/')
    def index():
        # Redirect the Request_url '/' to '/blog/'
        return redirect(url_for('main.home'))'''

    # Register the Blueprint into app object
    app.register_blueprint(main)
    app.register_blueprint(auth,url_prefix='/auth')
    return app