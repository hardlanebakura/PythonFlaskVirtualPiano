from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint, abort
from flask_cors import CORS, cross_origin
from subsidiary_functions import *
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from log_config import logging
import time

learn_teach_pages = Blueprint('learn_teach', __name__,
                        template_folder='Templates', static_folder='static', url_prefix = "/")

@learn_teach_pages.route('/learn_teach', methods = ["GET", "POST"])
def learn_teach():
    learn_teach_users = LearnTeach.query.all()
    if request.method == "POST":
        if request.form['submit'] == "LEARN_TEACH":
            logging.info(request.form["learn_teach"])
            lt = LearnTeach(username = current_user.username, is_searching = request.form["learn_teach"])
            db.session.add(lt)
            db.session.commit()
            return redirect(request.url)
    if current_user.is_anonymous:
        return render_template("learn_teach.html", learn_teach_users = learn_teach_users)
    return render_template("learn_teach.html", loggedinuser = current_user.username, learn_teach_users = learn_teach_users, admin = current_user.isadmin)



