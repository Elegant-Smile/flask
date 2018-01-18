from datetime import datetime

from tigereye.models import db, Model
from sqlalchemy import text
from enum import Enum, unique


@unique
class SeatStatus(Enum):
    """正常状态，可购买"""
    ok = 0
    """已锁定"""
    locked = 1
    """已售出"""
    sold = 2
    """已打票"""
    printed = 3
    """已预订"""
    booked = 9
    """维修中"""
    repair = 99


@unique
class SeatType(Enum):
    """过道"""
    road = 0
    """单人"""
    single = 1
    """双人"""
    couple = 2
    """保留座位"""
    reserve = 3
    """残疾专座"""
    for_disable = 4
    """VIP专座"""
    vip = 5
    """震动座椅"""
    shake = 6
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
#     桌位id,sid
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

    @classmethod
    # 类方法,能直接被类. 调用
    def lock(cls, orderno, pid, sid):
        # 事物
        session = db.create_scoped_session()
        # query能直接放对象吗?<sql:query>标签用来运行SQL SELECT语句，
        # filter用类名.属性名，比较用==，filter_by直接用属性名，比较用=
        # rows 是链式调用返回的修改数
        rows = session.query(PlaySeat).filter(

            PlaySeat.pid == pid,
            # Seatstatus 自定义类方法
            PlaySeat.status == SeatStatus.ok.value,
            # sqlalchemy in语法查询，查询id 在一个list里的所有集合
            PlaySeat.sid.in_(sid)
        ).update({
            'orderno': orderno,
            'status': SeatStatus.locked.value,
            'lock_time': datetime.now()
            # 属于 update 的参数 synchronize_session用于query在进行delete or update操作时，对session的同步策略。
            # False - 不对session进行同步，直接进行delete or update操作。
        }, synchronize_session=False)
        if rows != len(sid):
            session.rollback()
            return 0
        session.commit()
        return rows

    @classmethod
    def unlock(cls, orderno, pid, sid):
        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter_by(
            orderno=orderno,
            status=SeatStatus.locked.value).update({
            'orderno': None,
            'status': SeatStatus.ok.value,
        })
        if rows != len(sid):
            session.rollback()
            # 返回的是0,
            return 0
        session.commit()
        return rows
