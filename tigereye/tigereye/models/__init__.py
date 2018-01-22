from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask import json as _json

db = SQLAlchemy()


# 自定义了这样一个类,简化数据库操作
class Model(object):
    @classmethod
    def get(cls, primary_key):
        return cls.query.get(primary_key)

    def put(self):
        db.session.add(self)

    @classmethod
    #  classmethod 修饰符对应的函数不需要实例化，不需要 self 参数，
    # 但第一个参数需要是表示自身类的 cls 参数，可以来调用类的属性，类的方法，
    # commit 和rollback 为何要 这儿定义类方法, 是因为 可以多次push 然后一次提交,提高代码运行速率
    def commit(cls):
        db.session.commit()

    @classmethod
    def rollback(cls):
        db.session.rollback()

    def delete(self):
        db.session.delete(self)

    def save(self):
        try:
            self.put()
            self.commit()
        except Exception:
            self.rollback()
            raise

    def __json__(self):
        # vars():函数以字典形式返回参数中每个成员的当前值
        # keys = vars(self).keys()
        data = {}
        for k, v in vars(self).items():
            if k.startswith('_'):
                continue
            if isinstance(v, datetime):
                v = v.strftime('%Y%m%d%H%M%S')
            data[k] = v
        # print(data)
        return data


# _json是因为系统也这么喊,源码可证明,要替换 掉系统的方法
class JSONEncoder(_json.JSONEncoder):
    # o是movie的对象
    def default(self, o):
        # 只要是db.Model的对象,就返回o.__json__
        # isinstance 判断对象的类型,如果是是我们自己建的对象,db是自己实例化的sql对象,然后自定义了model,一,为了简化数据库的操作
        # 二,我们自己建立的对象都多继承了 这个model类,所以我们自己建立的对象都直接被自定义的方法转换为字典了.
        # 如果 不是我们自己定义的对象,就还是调用系统的方法 .
        if isinstance(o, db.Model):
            # 为什么是o.__json(),因为自定义了一个类,又在这个类里自定以了一个__json__方法,所以才能这么用
            return o.__json__()
        # 如果不是就调用自己本身的方法
        return _json.JSONEncoder.default(self, o)
