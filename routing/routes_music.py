from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint, abort
from flask_cors import CORS, cross_origin
from jinja2 import TemplateNotFound
from subsidiary_functions import *
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from log_config import logging
import time
import os

music_pages = Blueprint('music', __name__,
                        template_folder='Templates/music/', static_folder='static', url_prefix = "/music")

@music_pages.route('/', methods = ["POST"])
def music_post():
    if request.form['submit'] == "POST SONG REQUEST":
        song_request_content = request.form['song_request']
        song_request = Comment(content = song_request_content, author = current_user.username)
        db.session.add(song_request)
        db.session.commit()
        return redirect(request.url)

@music_pages.route('/')
def music():
    if current_user.is_anonymous:
        return render_template("music_sheets.html", comments = get_comments(), latest_music = get_latest_music())
    return render_template("/music/music_sheets.html", loggedinuser=current_user.username, avatar = get_avatar_for_a_user(current_user.username), comments = get_comments(), latest_music = get_latest_music(),
                           admin = is_admin(current_user.username))

@music_pages.route('/genres')
def genres():
    if current_user.is_anonymous:
        return render_template("music/genres.html")
    return render_template("music/genres.html", loggedinuser = current_user.username, admin = current_user.isadmin)

@music_pages.route('/genres/<string:genre>')
def sheets_genre(genre):
    if current_user.is_anonymous:
        return render_template("music/genre.html", genre = genre, music_sheets_for_genre = get_music_sheets_for_genre(genre))
    return render_template("music/genre.html", loggedinuser = current_user.username, genre = genre, music_sheets_for_genre = get_music_sheets_for_genre(genre), admin = current_user.isadmin)

@music_pages.route('/sort_genres', methods = ["GET", "POST"])
@login_required
def sort_genres():
    #admins sort out genres of existing sheets
    music_sheets = []
    for i in range(len(MusicSheet.query.all())):
        dict1 = vars(MusicSheet.query.all()[i])
        music_sheets.append(dict1)
    return render_template("music/sort_genres.html", music_sheets = music_sheets, loggedinuser = current_user.username, admin = is_admin(current_user.username))

@music_pages.route('/artists')
def artists():
    letter = request.args.get('letter')
    music_artists = get_artists_letter(letter)
    if current_user.is_anonymous:
        return render_template("music/artists.html", letter = letter, music_artists = music_artists)
    return render_template("music/artists.html", loggedinuser = current_user.username, letter=letter,
                           music_artists=music_artists)

@music_pages.route('/artists/<string:artist>')
def artist(artist):
    music_sheets_by_artist = get_music_sheets_by_artist(artist)
    if current_user.is_anonymous:
        return render_template("music/artist.html", artist = artist, music_sheets_by_artist =  music_sheets_by_artist)
    return render_template("music/artist.html", loggedinuser = current_user.username, artist = artist, music_sheets_by_artist = music_sheets_by_artist)

@music_pages.route('/sheets')
def music_sheets():
    letter = request.args.get('letter')
    music_sheets = get_music_sheets_letter(letter)
    logging.info(music_sheets)
    if current_user.is_anonymous:
        return render_template("music/sheets.html", letter = letter, music_sheets = music_sheets)
    return render_template("music/sheets.html", loggedinuser = current_user.username, letter = letter, music_sheets = music_sheets)

@music_pages.route('/sheets/<int:sheet_id>')
def music_sheet(sheet_id):
    music_sheet = vars(MusicSheet.query.filter_by(id = sheet_id).first())
    if current_user.is_anonymous:
        return render_template("music_sheet.html", music_sheet = music_sheet)
    return render_template("music/music_sheet.html", loggedinuser = current_user.username, music_sheet = music_sheet)

@music_pages.route('/sheets/edit/<int:id>', methods = ["GET", "POST"])
def edit_sheet(id):
    sheet = MusicSheet.query.get_or_404(id)
    if request.method == "POST":
        return render_template("/edit_genres.html", sheet = sheet)
    return render_template("/edit_genres.html", sheet = sheet)

@music_pages.route('/sheets/update/<int:id>', methods = ["GET", "POST"])
def update_sheet(id):
    sheet = MusicSheet.query.get_or_404(id)
    author = sheet.author
    if request.method == "POST":
        selected_option = request.form.get("update_genres_select")
        sheet.genre = selected_option
        db.session.add(sheet)
        db.session.commit()
        return redirect("/sort_genres")
    return render_template("/update_genres.html", loggedinuser = current_user.username, admin = current_user.isadmin)

@music_pages.route('/sheets/delete/<int:id>')
def delete_sheet(id):
    sheet = MusicSheet.query.get_or_404(id)
    db.session.delete(sheet)
    db.session.commit()
    return redirect('/sort_genres')
