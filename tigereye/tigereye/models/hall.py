from tigereye.models import db


class Hall(db.Model):
    hid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer)
    name = db.Column(db.String(64), unique=True, nullable=False)
    screen = db.Column(db.String(32))
    #音效
    auto_type = db.Column(db.String(32))
    #座位数量
    seats_num = db.Column(db.Integer, default=0, nullable=False)
    #状态
    status = db.Column(db.Integer, nullable=False, index=True)
