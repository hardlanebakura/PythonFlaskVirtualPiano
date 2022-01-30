from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint, abort
from jinja2 import TemplateNotFound
from log_config import logging
from routing.routes_index import index_page

login_page = Blueprint('login', __name__,
                        template_folder='Templates', static_folder='static')

@login_page.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect("/")
    return render_template("login.html")