from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint, abort, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

logout_pages = Blueprint('logout', __name__,
                        template_folder='Templates', static_folder='static', url_prefix = "/")

@logout_pages.route('/logout', methods = ["GET", "POST"])
def logout():
    user = current_user.username
    logout_user()
    flash("User {} has been successfully logged out.".format(user))
    return redirect("/")
