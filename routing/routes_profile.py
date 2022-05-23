from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint, abort
from flask_cors import CORS, cross_origin
from subsidiary_functions import *
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from log_config import logging
import os

profile_pages = Blueprint('profile', __name__,
                        template_folder='Templates/', static_folder='static', url_prefix = "/")

@profile_pages.route('/profile', methods = ["GET", "POST"])
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
