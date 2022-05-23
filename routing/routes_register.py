from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint, abort
from flask_cors import CORS, cross_origin
from subsidiary_functions import *
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from log_config import logging
from dotenv import dotenv_values

ADMINS = dotenv_values("admins.env")["ADMINS"]

register_pages = Blueprint('register', __name__,
                        template_folder='Templates/', static_folder='static', url_prefix = "/")

@register_pages.route('/register', methods = ["POST"])
def register_post():
    email = request.form["register_email"]
    username = request.form["register_username"]
    password = request.form["register_password1"]
    logging.debug(email, username, password)
    nu = User(email=email, username=username, password=password)
    if nu.username in ADMINS:
        nu.isadmin = True
    user_exists = len(db.session.query(User).filter_by(email=nu.email).all()) > 0 and len(
        db.session.query(User).filter_by(username=nu.username).all()) > 0
    logging.debug(user_exists)
    if not user_exists:
        db.session.add(nu)
        db.session.commit()
        login_user(nu)
    # db.session.add(nu)
    # db.session.commit()

    return redirect("/")

@register_pages.route('/register')
def register():
    logging.debug(all_users)
    return render_template("register.html", all_users=all_users)
