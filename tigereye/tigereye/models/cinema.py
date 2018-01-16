from tigereye.models import db


class Cinema(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    address = db.Column(db.String(256), nullable=False)
    #影厅数量
    halls = db.Column(db.Integer, default=0, nullable=False)
    #手续费
    handle_fee = db.Column(db.Integer, default=0, nullable=False)
    #购买限制
    buy_limit = db.Column(db.Integer, default=0, nullable=False)
    # 状态有个索引
    status = db.Column(db.Integer, nullable=False, index=True)

