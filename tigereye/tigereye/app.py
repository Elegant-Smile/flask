from logging import FileHandler, Formatter
import logging
from logging.handlers import SMTPHandler

from flask import Flask
from tigereye.models import db, JSONEncoder
from flask_classy import FlaskView
import os


def create_app(config=None):
    app = Flask(__name__)
    # app.debug = debug
    # 我们平时用的app.config.from_object(config[你自己定义的config字典key名字])才能运行！！！
    # 另外，记住，config([你自己定义的config字典])，他为什么可以找到，是因为，在程序头上，我们已经定义了from config import config!!!
    app.config.from_object('tigereye.configs.default.DefalutConfig')
    app.config.from_object(config)
    # 替换掉json 的encoder方法
    app.json_encoder = JSONEncoder
    # 只有不是在debug的情况下启用
    if not app.debug:
        app.logger.setLevel(logging.INFO)
        mail_handler = SMTPHandler(
            app.config['EMAIL_HOST'],
            app.config['SERVER_EMAIL'],
            app.config['ADMINS'],
            'TIGEREYE ALERT',
            credentials=(app.config['EMAIL_HOST_USER'],
                         app.config['EMAIL_HOST_PASSWORD'])
        )
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(Formatter("""
        Message Type: %(levelname)s
        Location:     %(pathname)s: %(lineno)d
        Module:       %(module)s
        Function:     %(funcName)s
        Time:         %(asctime)s
        Message:    %(message)s    """))
        app.logger.addHandler(mail_handler)

        file_handler = FileHandler(os.path.join(app.config['LOG_DIR'], 'app.log'))
        file_handler.setLevel(logging.INFO)
        # 定义handler的输出格式
        file_handler.setFormatter(Formatter(
            '%(asctime)s %(levelname)s : %(message)s'
        ))
        app.logger.addHandler(file_handler)

    # 初始化数据库
    db.init_app(app)
    # 自定义的方法,注册了所有的view
    configure_view(app)
    app.logger.info('creat app succ ')
    return app


def configure_view(app):
    from tigereye.api.cinema import CinemaView
    from tigereye.api.misc import MiscView
    from tigereye.api.movie import MovieView
    from tigereye.api.hall import HallView
    from tigereye.api.play import PlayView
    from tigereye.api.seat import SeatView
    from tigereye.api.order import OrderView
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
