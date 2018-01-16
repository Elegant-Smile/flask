from flask_sqlalchemy import SQLAlchemy
from flask import json as _json

db = SQLAlchemy()


# _json是为了不和系统的json重复,定义了一个类,要替换 掉系统的方法
class JSONEncoder(_json.JSONEncoder):
    # o是movie的对象
    def default(self, o):
        # 只要是db.Model的对象,就返回o.__json__
        if isinstance(0, db.Model):

            return o.__json__()
        # 如果不是就调用自己本身的方法
        return _json.JSONEncoder.default(self, o)
