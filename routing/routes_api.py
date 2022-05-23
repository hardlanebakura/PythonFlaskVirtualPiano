from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint, abort
from flask_cors import CORS, cross_origin
from subsidiary_functions import *
from keys import keyboard_notes, keyboard_sounds
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from log_config import logging
import time
import os

api_pages = Blueprint('api', __name__,
                        template_folder='Templates', static_folder='static', url_prefix = "/api")

@api_pages.route("/")
def api():
    all_users = User.find_all()
    return jsonify({"All routes": [{"all_users":"/api/all_users", "all_sheets":"/api/all_sheets", "all_comments":"/api/all_comments"}]})

@api_pages.route("/all_users")
def all_users():
    all_users = User.find_all()
    return jsonify({"all_users": all_users})

@api_pages.route("/all_sheets")
def all_sheets():
    all_sheets = MusicSheet.find_all()
    return jsonify({"all_sheets": all_sheets})

@api_pages.route("/all_comments")
def all_():
    all_comments = Comment.find_all()
    return jsonify({"all_comments": all_comments})



