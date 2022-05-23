from subsidiary_functions import *
from routing.routes import index_pages
from routing.routes_upload import upload_pages
from routing.routes_message import message_pages
from routing.routes_inbox import inbox_pages
from routing.routes_music import music_pages
from routing.routes_learn_teach import learn_teach_pages
from routing.routes_login import login_pages
from routing.routes_register import register_pages
from routing.routes_profile import profile_pages
from routing.routes_logout import logout_pages
from routing.routes_api import api_pages

app.register_blueprint(index_pages)
app.register_blueprint(upload_pages)
app.register_blueprint(message_pages)
app.register_blueprint(inbox_pages)
app.register_blueprint(music_pages)
app.register_blueprint(learn_teach_pages)
app.register_blueprint(login_pages)
app.register_blueprint(register_pages)
app.register_blueprint(profile_pages)
app.register_blueprint(logout_pages)
app.register_blueprint(api_pages)

if (__name__ == "__main__"):
    app.run(debug = True)