def set_config(dict, env):
    #setting app.config
    dict['SECRET_KEY'] = 'secretkey1'
    dict['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
    dict['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    dict['SQLALCHEMY_BINDS'] = {"avatars": "sqlite:///avatars.db", "music_sheets": "sqlite:///music_sheets.db", "comments": "sqlite:///comments.db", "messages": "sqlite:///messages.db", "learn_teach_users": "sqlite:///learn_teach.db"}
    dict['TEMPLATES_AUTO_RELOAD'] = True
    dict["CACHE_TYPE"] = "redis"
    dict['UPLOAD_PATH'] = "C:\\Users\dESKTOP I5\PycharmProjects\\PythonFlaskVirtualPiano\\static\\uploads\\images"
    dict['UPLOAD_MUSIC_PATH'] = "C:\\Users\dESKTOP I5\PycharmProjects\\PythonFlaskVirtualPiano\\static\\uploads\\music"
    dict['DEFAULT_AVATAR'] = "C:\\Users\dESKTOP I5\PycharmProjects\\PythonFlaskVirtualPiano\\static\\images\\login-icon.jpg"

    # setting jinja_env
    env.auto_reload = True
    env.cache = {}





