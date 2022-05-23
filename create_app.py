from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from config import *
from datetime import datetime
from log_config import logging
from keys import keyboard_notes, keyboard_sounds
from flask_cors import CORS, cross_origin
from db_models import *
import os
from operator import itemgetter
from dotenv import dotenv_values

#from routing.routes import *
import time

ADMINS = dotenv_values("admins.env")["ADMINS"]

def create_app():
    app = Flask(__name__, template_folder = "Templates")

    set_config(app.config, app.jinja_env)

    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.app_context().push()
    SESSION_TYPE = 'sqlalchemy'
    app.config.from_object(__name__)

    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app