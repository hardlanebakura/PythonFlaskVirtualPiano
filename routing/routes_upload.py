from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint, abort
from flask_cors import CORS, cross_origin
from jinja2 import TemplateNotFound
from subsidiary_functions import *
from keys import keyboard_notes, keyboard_sounds
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from log_config import logging
import time
import os

upload_pages = Blueprint('upload', __name__,
                        template_folder='Templates', static_folder='static')

@upload_pages.route("/upload", methods = ["POST"])
@cross_origin()
@login_required
def upload_post():
    if request.method == "POST":
        if request.form['submit'] == "UPLOAD_MUSIC":
            uploaded_sheet = request.files['UPLOAD_MUSIC']
            uploaded_sheet_title = uploaded_sheet.filename
            if uploaded_sheet_title != "":
                uploaded_sheet_content = uploaded_sheet.read()
                uploaded_sheet.save(os.path.join(app.config["UPLOAD_MUSIC_PATH"], uploaded_sheet.filename))
                sheet = MusicSheet(title = uploaded_sheet_title, content = uploaded_sheet_content, author = current_user.username)
                db.session.add(sheet)
                db.session.commit()
                return redirect(request.url)
            else:
                return redirect(request.url)

@upload_pages.route("/upload")
@cross_origin()
@login_required
def upload():
    return render_template("upload.html", loggedinuser = current_user.username, admin = is_admin(current_user.username))