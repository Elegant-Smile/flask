from flask import Flask
from tigereye.models import db, JSONEncoder
from flask_classy import FlaskView


def create_app(debug=True):
    app = Flask(__name__)
    # app.debug = debug
    app.config.from_object('tigereye.configs.default.DefalutConfig')

    app.json_encoder = JSONEncoder
    # 替换掉json 的encoder方法

    # 自定义的方法,注册了所有的view
    configure_view(app)
    # 初始化数据库
    db.init_app(app)
    return app


def configure_view(app):
    from tigereye.api.cinema import CinemaView
    from tigereye.api.misc import MiscView
    from tigereye.api.movie import MovieView
    from tigereye.api.hall import HallView
    from tigereye.api.play import PlayView
    from tigereye.api.seat import SeatView

    # locals()函数会以dict类型返回当前位置的全部局部变量。
    for view in locals().values():
        # 判断是对象还是类,type(CinemaView)=type,type是超类,所有类的父类,
        # type(app) = flask
        if type(view) == type and issubclass(view, FlaskView):
            view.register(app)
            # 这样就不用每个试图都注册了
            # 自定义了api方法,就要在这里注册
            # MiscView.register(app)
            # CinemaView.register(app)
            # MovieView.register(app)
