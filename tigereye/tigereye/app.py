from flask import Flask
from tigereye.models import db, JSONEncoder
from tigereye.api.cinema import CinemaView
from tigereye.api.misc import MiscView
from tigereye.api.movie import MovieView

def create_app(debug=True):
    app = Flask(__name__)
    # app.debug = debug
    app.config.from_object('tigereye.configs.default.DefalutConfig')

    app.json_encoder = JSONEncoder
    # 替换掉json 的encoder方法

    MiscView.register(app)
    CinemaView.register(app)
    MovieView.register(app)
    #初始化数据库
    db.init_app(app)
    return app
