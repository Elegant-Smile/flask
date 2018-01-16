from flask_sqlalchemy import SQLAlchemy
from flask import json as _json
db = SQLAlchemy()
#_json是为了不和系统的json重复
class JSONEncoder(_json.JSONEncoder):
    def defult(self,o):
        if isinstance(0,db.Model):
            return o.__json__()
        return _json.JSONEncoder.default(self,o)