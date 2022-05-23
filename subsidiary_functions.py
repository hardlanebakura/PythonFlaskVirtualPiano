from config import *
from db_models import *
from log_config import logging
from operator import itemgetter
from create_app import create_app

app = create_app()


for i in range(len(Avatar.query.all())):
    dict1 = vars(Avatar.query.all()[i]).copy()

users_amount = len(db.session.query(User).all())

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