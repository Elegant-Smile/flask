from tigereye.models import db, Model


# 影厅
#     id
#     影院id
#     名称
#     屏幕类型
#     音效  audio_type
#     座位数量
#     状态

class Hall(db.Model, Model):
    hid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer)
    name = db.Column(db.String(200), nullable=False)
    screen_type = db.Column(db.String(32))
    audio_type = db.Column(db.String(32))
    seatus_num = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.Integer, default=0, index=True, nullable=False)
