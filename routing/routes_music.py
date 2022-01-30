from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint, abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from jinja2 import TemplateNotFound
from log_config import logging

music_page = Blueprint('music', __name__,
                        template_folder='Templates', static_folder='static')

@music_page.route('/music', methods = ["GET", "POST"])
def music():
    if request.method == "POST":
        return redirect(request.url)
    if current_user.is_anonymous:
        try:
            return render_template("music/music_sheets.html")
        except TemplateNotFound:
            abort(404)
    try:
        return render_template("music/music_sheets.html", loggedinuser=current_user.username, current_user = current_user)
    except TemplateNotFound:
        abort(404)

@music_page.route('/music/genres')
def genres():
    if current_user.is_anonymous:
        try:
            return render_template("music/genres.html")
        except TemplateNotFound:
            abort(404)
    try:
        return render_template("music/genres.html", loggedinuser=current_user.username)
    except TemplateNotFound:
        abort(404)