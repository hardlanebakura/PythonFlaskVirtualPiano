from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint, abort
from flask_cors import CORS, cross_origin
from jinja2 import TemplateNotFound
from log_config import logging

index_pages = Blueprint('index', __name__,
                        template_folder='Templates', static_folder='static')

@index_pages.route("/")
@cross_origin()
def index():
    logging.info(get_music_sheets_letter("A"))
    logging.info(get_most_active_users())
    latest_music = get_latest_music()
    loaded_music_sheet = request.args.get("loaded_sheet")
    if loaded_music_sheet != None:
        loaded_sheet = MusicSheet.query.filter_by(title = loaded_music_sheet + ".txt").first()
    else: loaded_sheet = None
    if current_user.is_anonymous:
        return render_template("index.html", keyboard_notes = keyboard_notes, keyboard_sounds = keyboard_sounds, latest_music = latest_music,
                               loaded_sheet = loaded_sheet, latest_users = get_latest_users(), most_active_users = get_most_active_users())
    avatar = get_avatar_for_a_user(current_user.username)
    logging.info(request.args.get("avatar"))
    logging.info("--- %s seconds ---" % (time.time() - start_time))
    return render_template("index.html", loggedinuser = current_user.username, keyboard_notes = keyboard_notes, keyboard_sounds = keyboard_sounds, avatar = avatar, latest_music = latest_music,
                           loaded_sheet = loaded_sheet, latest_users = get_latest_users(), most_active_users = get_most_active_users(), admin = current_user.isadmin)