from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from config import *
from datetime import datetime
from log_config import logging
from keys import keyboard_notes, keyboard_sounds
from flask_cors import CORS, cross_origin
from db_models import *
import os
from operator import itemgetter
from dotenv import dotenv_values

from subsidiary_functions import *
from routing.routes import *
import time

ADMINS = dotenv_values("admins.env")["ADMINS"]

start_time = time.time()

app.register_blueprint(index_pages)

@app.route("/upload", methods = ["GET", "POST"])
@login_required
def upload():
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
    return render_template("upload.html", loggedinuser = current_user.username, admin = is_admin(current_user.username))

@app.route("/compose_message", methods = ["GET", "POST"])
@login_required
def compose_message():
    if request.method == "POST":
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
    return render_template("compose_message.html", loggedinuser = current_user.username, recipient = request.args.get("recipient"))

@app.route('/inbox')
def inbox():
    inbox_messages = get_inbox_messages_for_user(current_user.username)
    return render_template("inbox.html", loggedinuser = current_user.username, inbox_messages = inbox_messages, avatar = get_avatar_for_a_user(current_user.username), all_emails = get_all_emails())

@app.route('/music', methods = ["GET", "POST"])
def music():
    if request.method == "POST":
        if request.form['submit'] == "POST SONG REQUEST":
            song_request_content = request.form['song_request']
            song_request = Comment(content = song_request_content, author = current_user.username)
            db.session.add(song_request)
            db.session.commit()
            return redirect(request.url)
    if current_user.is_anonymous:
        return render_template("music/music_sheets.html", comments = get_comments(), latest_music = get_latest_music())
    return render_template("music/music_sheets.html", loggedinuser=current_user.username, avatar = get_avatar_for_a_user(current_user.username), comments = get_comments(), latest_music = get_latest_music(),
                           admin = is_admin(current_user.username))

@app.route('/music/genres')
def genres():
    if current_user.is_anonymous:
        return render_template("music/genres.html")
    return render_template("music/genres.html", loggedinuser = current_user.username, admin = current_user.isadmin)

@app.route('/music/genres/<string:genre>')
def sheets_genre(genre):
    if current_user.is_anonymous:
        return render_template("music/genre.html", genre = genre, music_sheets_for_genre = get_music_sheets_for_genre(genre))
    return render_template("music/genre.html", loggedinuser = current_user.username, genre = genre, music_sheets_for_genre = get_music_sheets_for_genre(genre), admin = current_user.isadmin)

@app.route('/music/sort_genres', methods = ["GET", "POST"])
@login_required
def sort_genres():
    #admins sort out genres of existing sheets
    music_sheets = []
    for i in range(len(MusicSheet.query.all())):
        dict1 = vars(MusicSheet.query.all()[i])
        music_sheets.append(dict1)
    return render_template("music/sort_genres.html", music_sheets = music_sheets, loggedinuser = current_user.username, admin = is_admin(current_user.username))

@app.route('/music/artists')
def artists():
    letter = request.args.get('letter')
    music_artists = get_artists_letter(letter)
    if current_user.is_anonymous:
        return render_template("music/artists.html", letter = letter, music_artists = music_artists)
    return render_template("music/artists.html", loggedinuser = current_user.username, letter=letter,
                           music_artists=music_artists)

@app.route('/music/artists/<string:artist>')
def artist(artist):
    music_sheets_by_artist = get_music_sheets_by_artist(artist)
    if current_user.is_anonymous:
        return render_template("music/artist.html", artist = artist, music_sheets_by_artist =  music_sheets_by_artist)
    return render_template("music/artist.html", loggedinuser = current_user.username, artist = artist, music_sheets_by_artist = music_sheets_by_artist)

@app.route('/music/sheets')
def music_sheets():
    letter = request.args.get('letter')
    music_sheets = get_music_sheets_letter(letter)
    logging.info(music_sheets)
    if current_user.is_anonymous:
        return render_template("music/sheets.html", letter = letter, music_sheets = music_sheets)
    return render_template("music/sheets.html", loggedinuser = current_user.username, letter = letter, music_sheets = music_sheets)

@app.route('/music/sheets/<int:sheet_id>')
def music_sheet(sheet_id):
    music_sheet = vars(MusicSheet.query.filter_by(id = sheet_id).first())
    if current_user.is_anonymous:
        return render_template("music/music_sheet.html", music_sheet = music_sheet)
    return render_template("music/music_sheet.html", loggedinuser = current_user.username, music_sheet = music_sheet)

@app.route('/music/sheets/edit/<int:id>', methods = ["GET", "POST"])
def edit_sheet(id):
    sheet = MusicSheet.query.get_or_404(id)
    if request.method == "POST":
        return render_template("/music/edit_genres.html", sheet = sheet)
    return render_template("/music/edit_genres.html", sheet = sheet)

@app.route('/music/sheets/update/<int:id>', methods = ["GET", "POST"])
def update_sheet(id):
    sheet = MusicSheet.query.get_or_404(id)
    author = sheet.author
    if request.method == "POST":
        selected_option = request.form.get("update_genres_select")
        sheet.genre = selected_option
        db.session.add(sheet)
        db.session.commit()
        return redirect("/music/sort_genres")
    return render_template("/music/update_genres.html", loggedinuser = current_user.username, admin = current_user.isadmin)

@app.route('/music/sheets/delete/<int:id>')
def delete_sheet(id):
    sheet = MusicSheet.query.get_or_404(id)
    db.session.delete(sheet)
    db.session.commit()
    return redirect('/music/sort_genres')

@app.route('/learn_teach', methods = ["GET", "POST"])
def learn_teach():
    learn_teach_users = LearnTeach.query.all()
    if request.method == "POST":
        if request.form['submit'] == "LEARN_TEACH":
            logging.info(request.form["learn_teach"])
            lt = LearnTeach(username = current_user.username, is_searching = request.form["learn_teach"])
            db.session.add(lt)
            db.session.commit()
            return redirect(request.url)
    if current_user.is_anonymous:
        return render_template("learn_teach.html", learn_teach_users = learn_teach_users)
    return render_template("learn_teach.html", loggedinuser = current_user.username, learn_teach_users = learn_teach_users, admin = current_user.isadmin)

@app.route("/login/", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username_1"]
        password = request.form["password_1"]
        check_login = User.query.filter_by(username="%s" % username).first()
        if (check_login == None):
            if (current_user.is_anonymous):
                return render_template("login.html", handle = 1)
        passwords_match = check_login.password == password
        if (check_login):
            if not passwords_match:
                logging.debug("Passwords didnt match")
                return render_template("login.html", handle = 2)
            else:
                logging.debug("Passwords matching!")
                login_user(check_login)
                return redirect("/")
        return redirect("/")

    return render_template("login.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["register_email"]
        username = request.form["register_username"]
        password = request.form["register_password1"]
        logging.debug(email, username, password)
        nu = User(email=email, username=username, password=password)
        if nu.username in ADMINS:
            nu.isadmin = True
        user_exists = len(db.session.query(User).filter_by(email = nu.email).all()) > 0 and len(db.session.query(User).filter_by(username = nu.username).all()) > 0
        logging.debug(user_exists)
        if not user_exists:
            db.session.add(nu)
            db.session.commit()
            login_user(nu)
        #db.session.add(nu)
        #db.session.commit()

        return redirect("/")
    logging.debug(all_users)
    return render_template("register.html", all_users = all_users)

@app.route("/profile", methods = ["GET", "POST"])
@login_required
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

@app.route("/logout")
@login_required
def logout():
    user = current_user.username
    logout_user()
    flash("User {} has been successfully logged out.".format(user))
    return redirect("/")

if (__name__ == "__main__"):
    app.run(debug = True)