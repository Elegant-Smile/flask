from flask import Flask
from tigereye.models import db
from tigereye.api.cinema import CinemaView
from tigereye.api.misc import MiscView
from tigereye.configs.default import DefalutConfig

def create_app(debug=True):
    app = Flask(__name__)
    # app.debug = debug
    app.config.from_object('tigereye.configs.default.DefalutConfig')
    #
    MiscView.register(app)
    CinemaView.register(app)
    #初始化数据库
    db.init_app(app)
    return app
