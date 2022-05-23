from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint, abort
from flask_cors import CORS, cross_origin
from jinja2 import TemplateNotFound
from subsidiary_functions import *
from keys import keyboard_notes, keyboard_sounds
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from log_config import logging
import time
import os

inbox_pages = Blueprint('inbox', __name__,
                        template_folder='Templates', static_folder='static')

@inbox_pages.route("/inbox", methods = ["POST"])
@login_required
@app.route('/inbox')
def inbox():
    inbox_messages = get_inbox_messages_for_user(current_user.username)
    return render_template("inbox.html", loggedinuser = current_user.username, inbox_messages = inbox_messages, avatar = get_avatar_for_a_user(current_user.username), all_emails = get_all_emails())