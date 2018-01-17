from tigereye.models import db, Model
from sqlalchemy import text


# 座位
#     id
#     影院ID
#     影厅ID
#     座位类型   seat_type
#         是否是情侣座
#         x坐标
#         y坐标
#         排（A/第一排）
#         列（***）
#         区域
#     状态

class Seat(db.Model, Model):
    sid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer)
    hid = db.Column(db.Integer)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)

    row = db.Column(db.String(16))
    column = db.Column(db.String(16))

    area = db.Column(db.String(16))
    seat_type = db.Column(db.String(16))
    love_seats = db.Column(db.String(16))

    status = db.Column(db.Integer, default=0, index=True, nullable=False)


# 排期座位
#     id
#     订单号
#     排期id
#     影院id
#     影厅id
#     桌位id
#     座位类型
#           是否是情侣坐
#     x坐标
#     y坐标
#     排（A/第一排）
#     列（***）
#     区域
#     状态
#         创建时间
#         锁定时间
class PlaySeat(db.Model, Model):
    psid = db.Column(db.Integer, primary_key=True)
    orderno = db.Column(db.String(32), index=True)
    cid = db.Column(db.Integer)
    hid = db.Column(db.Integer)
    sid = db.Column(db.Integer)
    pid = db.Column(db.Integer)

    seat_type = db.Column(db.String(16))
    love_seats = db.Column(db.String(16))

    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    row = db.Column(db.String(16))
    column = db.Column(db.String(16))
    area = db.Column(db.String(16))

    status = db.Column(db.Integer, default=0, index=True, nullable=False)

    lock_time = db.Column(db.DateTime)
    created_time = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))

    def copy(self, seat):
        self.sid = seat.sid
        self.cid = seat.cid
        self.hid = seat.hid
        self.x = seat.x
        self.y = seat.y
        self.row = seat.row
        self.column = seat.column
        self.area = seat.area
        self.seat_type = seat.seat_type
        self.love_seats = seat.love_seats
        self.status = seat.status
