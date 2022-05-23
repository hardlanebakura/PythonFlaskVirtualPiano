from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint, abort
from flask_cors import CORS, cross_origin
from jinja2 import TemplateNotFound
from subsidiary_functions import *
from keys import keyboard_notes, keyboard_sounds
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from log_config import logging
import time
import os

message_pages = Blueprint('message', __name__,
                        template_folder='Templates', static_folder='static')

@message_pages.route("/compose_message", methods = ["POST"])
@login_required
def compose_message_post():
    if request.form['submit'] == "COMPOSE_MESSAGE":
        message_recipient = request.form['compose_message']
        message_content = request.form['message_content']
        if message_content != "" and len(User.query.filter_by(username = message_recipient).all()) > 0 and message_recipient != current_user.username:
            message = Message(content = message_content, author = current_user.username, recipient = message_recipient)
            db.session.add(message)
            db.session.commit()
            return redirect('/')
        else:
            errors = []
            if message_content == "":
                errors.append("Message content must not be empty")
            if len(User.query.filter_by(username = message_recipient).all()) == 0:
                errors.append("Username doesn't exist")
            if message_recipient == current_user.username:
                errors.append("Sending self message")
            return render_template("compose_message.html", loggedinuser = current_user.username, errors = errors, recipient = request.args.get("recipient"))

@message_pages.route("/compose_message")
@cross_origin()
def compose_message():
    return render_template("compose_message.html", loggedinuser = current_user.username, recipient = request.args.get("recipient"))
