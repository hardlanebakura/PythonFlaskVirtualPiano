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

from subsidiary_functions import *
from routing.routes import index_pages
from routing.routes_upload import upload_pages
from routing.routes_message import message_pages
from routing.routes_inbox import inbox_pages
from routing.routes_music import music_pages
from routing.routes_learn_teach import learn_teach_pages
from routing.routes_login import login_pages
from routing.routes_register import register_pages

import time

ADMINS = dotenv_values("admins.env")["ADMINS"]

start_time = time.time()

app.register_blueprint(index_pages)
app.register_blueprint(upload_pages)
app.register_blueprint(message_pages)
app.register_blueprint(inbox_pages)
app.register_blueprint(music_pages)
app.register_blueprint(learn_teach_pages)
app.register_blueprint(login_pages)
app.register_blueprint(register_pages)

@app.route("/profile", methods = ["GET", "POST"])
@login_required
def profile():
    loggedinuser = current_user.username
    profilecreated1 = current_user.datetime
    profilecreated = profilecreated1.strftime("%Y %m %d")
    user_has_avatar = not user_needs_avatar(current_user)
    admin = is_admin(loggedinuser)
    logging.info(user_has_avatar)
    if request.method == "POST":
        #user has no avatar yet
        if request.form['submit'] == "GET_AVATAR":
            profile_picture = request.files["profile_picture"]
            if profile_picture.filename != "":
                profile_picture.save(os.path.join(app.config["UPLOAD_PATH"], profile_picture.filename))
                new_avatar = Avatar(img_link = profile_picture.filename, img_username = loggedinuser)
                db.session.add(new_avatar)
                db.session.commit()
            else:
                return redirect(request.url)
            avatar = get_avatar_for_a_user(loggedinuser)
            return redirect(request.url)
        #user has avatar
        else:
            profile_picture = request.files["profile_picture"]
            if profile_picture.filename != "":
                profile_picture.save(os.path.join(app.config["UPLOAD_PATH"], profile_picture.filename))
                get_updates_on_avatar(loggedinuser, profile_picture.filename)
            else:
                return redirect(request.url)
            avatar = get_avatar_for_a_user(loggedinuser)
            return redirect(request.url)
    avatar = get_avatar_for_a_user(loggedinuser)
    logging.info(user_has_avatar)
    music_sheets = get_music_sheets_by_a_user(loggedinuser)
    inbox_messages = get_inbox_messages_for_user(current_user.username)
    return render_template("profile.html", loggedinuser=loggedinuser, profilecreated = profilecreated, isadmin = current_user.isadmin, user_has_avatar = user_has_avatar, avatar = avatar, music_sheets = music_sheets,
                           admin = admin, inbox_messages = inbox_messages)

@app.route("/logout")
@login_required
def logout():
    user = current_user.username
    logout_user()
    flash("User {} has been successfully logged out.".format(user))
    return redirect("/")

if (__name__ == "__main__"):
    app.run(debug = True)