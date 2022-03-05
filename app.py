from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from config import set_config
from datetime import datetime
from log_config import logging
from keys import keyboard_notes, keyboard_sounds
from flask_cors import CORS, cross_origin
import os
from operator import itemgetter
from admins import ADMINS
import time

app = Flask(__name__, template_folder = "Templates")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

set_config(app.config, app.jinja_env)

start_time = time.time()

db = SQLAlchemy(app)
SESSION_TYPE = 'sqlalchemy'
app.config.from_object(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.DateTime, default = datetime.utcnow)
    isadmin = db.Column(db.Boolean, default = False)

    def __repr__(self):
        return "User " + str(self.id)

class Avatar(db.Model):
    __bind_key__ = "avatars"
    id = db.Column(db.Integer, primary_key=True)
    img_link = db.Column(db.String(100), nullable=False)
    img_username = db.Column(db.String(100), nullable=False, unique=True)
    datetime = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return "Avatar " + str(self.id)

class MusicSheet(db.Model):
    __bind_key__ = "music_sheets"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100))
    datetime = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return "Music Sheet " + str(self.id)

class Comment(db.Model):
    __bind_key__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "Comment " + str(self.id)

class Message(db.Model):
    __bind_key__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    recipient = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "Message " + str(self.id)

class LearnTeach(db.Model):
    __bind_key__ = "learn_teach_users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    is_searching = db.Column(db.String(100))
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "Learn/Teach " + str(self.id)

for i in range(len(Avatar.query.all())):
    dict1 = vars(Avatar.query.all()[i]).copy()

users_amount = len(db.session.query(User).all())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_all_users():
    all_users = []
    for i in range(users_amount):
        dict1 = vars(User.query.all()[i]).copy()
        dict2 = dict1.copy()
        for item in dict1:
            if item != "username" and item != "password" and item != "email":
                del dict2[item]
        all_users.append(dict2)
    return all_users

all_users = get_all_users()


def user_needs_avatar(User1):
    if not isinstance(User1, User):
        raise TypeError("Expected User input")
    for i in range(len(db.session.query(Avatar).all())):
        avatar = vars(Avatar.query.all()[i]).copy()
        if avatar["img_username"] == User1.username:
            return False
    return True

def get_updates_on_avatar(username, new_link):
    if not isinstance(username, str) or not isinstance(new_link, str):
        raise TypeError("Expected string input")
    avatar = db.session.query(Avatar).filter_by(img_username = username).first()
    avatar.img_link = new_link
    db.session.commit()

def get_avatar_for_a_user(username):
    if not isinstance(username, str):
        raise TypeError('Expected string input')
    try:
        return db.session.query(Avatar).filter_by(img_username = username).all()[0].img_link
    except:
        return False

def get_music_sheets_by_a_user(username):
    if not isinstance(username, str):
        raise TypeError('Expected string input')
    try:
        sheets_by_a_user = len(db.session.query(MusicSheet).filter_by(author=username).all())
        return sheets_by_a_user
    except:
        return 0

def get_latest_music():
    all_sheets = MusicSheet.query.order_by(MusicSheet.datetime).all()
    all_sheets.reverse()
    return all_sheets

def get_users_with_most_sheets():
    users_with_most_sheets = [
        {
            {"username": user["username"], "sheets": get_music_sheets_by_a_user(user["username"])}
        }
        for user in all_users
    ]
    logging.info(users_with_most_sheets)
    users_with_most_sheets = sorted(users_with_most_sheets, key = itemgetter("sheets"), reverse=True)
    return users_with_most_sheets

def get_comments():
    comments = [vars(Comment.query.all()[i]).copy() for i in range(len(db.session.query(Comment).all()))]
    for comment in comments:
        comment["avatar"] = get_avatar_for_a_user(comment["author"])
    comments = sorted(comments, key = itemgetter("datetime"), reverse = True)
    return comments

def is_admin(username):
    if not isinstance(username, str):
        raise TypeError('Expected string input')
    return User.query.filter_by(username = username).first().isadmin

def get_all_emails():
    all_emails = [{User.query.all()[i].username:User.query.all()[i].email} for i in range(len(User.query.all()))]
    dict1 = dict((key, val) for k in all_emails for key, val in k.items())
    return dict1

def get_inbox_messages_for_user(username):
    if not isinstance(username, str):
        raise TypeError('Expected string input')
    inbox_messages_for_user = []
    for i in range(len(Message.query.all())):
        dict1 = vars(Message.query.all()[i]).copy()
        dict1.pop("_sa_instance_state", None)
        for item in dict1:
            logging.info(item)
        if dict1["recipient"] == username:
            dict1["avatar"] = get_avatar_for_a_user(dict1["author"])
            inbox_messages_for_user.append(dict1)
    return inbox_messages_for_user

def get_artists_letter(letter):
    artists_letter = []
    if not isinstance(letter, str):
        raise TypeError("Expected string input")
    if len(letter) > 1:
        raise ValueError("String is too long")
    for i in range(len(MusicSheet.query.all())):
        dict1 = vars(MusicSheet.query.all()[i])
        if (" - ") in dict1["title"]:
            if dict1["title"][0] == letter: #or dict1["title"][0] == letter.lower():
                dict1["title"] = dict1["title"].split(" - ")[0]
                if dict1["title"] not in artists_letter:
                    artists_letter.append(dict1["title"])
    return artists_letter

def get_music_sheets_by_artist(artist):
    music_sheets_by_artist = []
    for i in range(len(MusicSheet.query.all())):
        if (" - ") in MusicSheet.query.all()[i].title:
            artist_name = MusicSheet.query.all()[i].title.split(" - ")[0]
            if artist_name == artist:
                music_sheets_by_artist.append(MusicSheet.query.all()[i])
    return music_sheets_by_artist

def get_music_sheets_letter(letter):
    if not isinstance(letter, str):
        raise TypeError('Expected string input')
    if len(letter) > 1:
        raise ValueError("String is too long")
    music_sheets_for_letter = []
    for i in range(len(MusicSheet.query.all())):
        dict1 = vars(MusicSheet.query.all()[i])
        if (" - ") not in dict1["title"]:
            #get titles that start with both the lowercase and the uppercase
            if dict1["title"][0] == letter: #or dict1["title"][0] == letter.lower():
                music_sheets_for_letter.append(dict1)
        else:
            dict1["artist"] = dict1["title"].split(" - ")[0]
            dict1["title"] = dict1["title"].split(" - ")[1]
            if dict1["title"][0] == letter: #or dict1["title"][0] == letter.lower():
                music_sheets_for_letter.append(dict1)

    return music_sheets_for_letter

def get_music_sheets_for_genre(genre):
    if not isinstance(genre, str):
        raise TypeError('Expected string input')
    music_sheets_for_genre = []
    for i in range(len(MusicSheet.query.all())):
        dict1 = vars(MusicSheet.query.all()[i])
        if dict1["genre"] == genre:
            music_sheets_for_genre.append(dict1)
    return music_sheets_for_genre

def get_most_active_users():
    most_active_users = []
    for user in all_users:
        user["sheets"] = get_music_sheets_by_a_user(user["username"])
        user["comments"] = 1
        user["avatar"] = get_avatar_for_a_user(user["username"])
        if user["sheets"] > 0:
            most_active_users.append(user)
    most_active_users = sorted(most_active_users, key = itemgetter("sheets"), reverse = True)
    return most_active_users

def get_latest_users():
    users = User.query.order_by(User.datetime).all()
    users.reverse()
    for user in users:
        user = vars(user)
        user["avatar"] = get_avatar_for_a_user(user["username"])
    return users[:4]

@app.route("/")
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