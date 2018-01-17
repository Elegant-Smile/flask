from tigereye.models import db, Model
from sqlalchemy import text
from sqlalchemy import func


# 排期
#     id
#     影院id
#     影厅id
#     电影id
#
#     开始时间
#     创建时间
#     最后跟新时间
#     时长
#     价格类型
#     原价
#     售价
#     最低价
#     状太
class Play(db.Model, Model):
    pid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer)
    hid = db.Column(db.Integer)
    mid = db.Column(db.Integer)

    start_time = db.Column(db.DateTime, nullable=False)
    created_time = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_time = db.Column(db.DateTime, onupdate=func.now())

    duration = db.Column(db.Integer, default=0, nullable=False)

    price_type = db.Column(db.Integer)
    price = db.Column(db.Integer)
    market_price = db.Column(db.Integer)
    lowest_price = db.Column(db.Integer)

    status = db.Column(db.Integer, default=0, index=True, nullable=False)
