from enum import unique, Enum
from random import randint

from tigereye.helper import tetime
from tigereye.models import db, Model
from sqlalchemy import text
from sqlalchemy import func


@unique
class OrderStatus(Enum):
    """已锁座"""
    locked = 1
    """解锁"""
    unlocked = 2
    """自动解锁(超过一定时间未操作被系统自动解锁)"""
    auto_unlocked = 3
    """已支付"""
    paid = 4
    """已出票"""
    printed = 5
    """退款"""
    refund = 6


# 订单
#     id
#     影院id
#     影厅id
#     电影id
#     排期id
#     创建时间
#     票
#         票数
#         取票码
#         金额
#     状态
#         已支付
#             支付时间
#             取票时间
#         未支付
#
#         退票
#             退款时间
#     最后一次更新时间

class Order(db.Model, Model):
    __tablename__ = 'orders'
    # 订单id,自己的订单号
    oid = db.Column(db.String(32), primary_key=True)
    # 销售方订单号
    seller_order_no = db.Column(db.String(32), index=True)
    cid = db.Column(db.Integer)
    pid = db.Column(db.Integer)
    sid = db.Column(db.Integer)
    # 取票码
    ticket_flag = db.Column(db.String(64))

    # 票数
    ticket_num = db.Column(db.Integer)
    amount = db.Column(db.Integer)

    paid_time = db.Column(db.DateTime)
    printed_time = db.Column(db.DateTime)
    refund_time = db.Column(db.DateTime)
    created_time = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_time = db.Column(db.DateTime, onupdate=func.now())
    status = db.Column(db.Integer, default=0, index=True, nullable=False)

    # sid 座位id
    @classmethod
    def create(cls, cid, pid, sid):
        order = cls()
        order.oid = '%s%s%s' % (tetime.now(), randint(100000, 999999), pid)
        order.cid = cid
        order.pid = pid
        # 如果座位id是列表,就拼接成字符串
        if type(sid) == list:
            cls.join = ','.join(str(i) for i in sid)
            order.sid = cls.join
        else:
            order.sid = sid
        return order

    @classmethod
    def getby_orderno(cls, orderno):
        return Order.query.filter_by(seller_order_no=orderno).first()
