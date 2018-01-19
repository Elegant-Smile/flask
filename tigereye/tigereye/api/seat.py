from tigereye.extensions.validator import Validator, multi_int, multi_complex_int
from flask_classy import route
from flask import request
from datetime import datetime
from tigereye.api import ApiView
from tigereye.helper.code import Code
from tigereye.models.order import Order, OrderStatus
from tigereye.models.play import Play
from tigereye.models.seat import PlaySeat, SeatType


class SeatView(ApiView):
    # 这个validator 过滤 传了很多参数
    @Validator(pid=int, sid=multi_int, price=int, orderno=str)
    # route() 装饰器把一个函数绑定到对应的 URL 上。
    @route('/lock/', methods=['POST'])
    def lock(self):
        # 使用Request.Params["id"]来获取参数是一种比较有效的途径。
        pid = request.params['pid']
        sid = request.params['sid']

        price = request.params['price']
        orderno = request.params['orderno']
        # 获取到场次
        play = Play.get(pid)
        if not play:
            return Code.play_does_not_exist, request.params
        if price < play.lowest_price:
            return Code.prcice_less_than_the_lowest_price, request.params
            # lock 是定义这个类,创建的而方法
        locked_seats_num = PlaySeat.lock(orderno, pid, sid)
        # 如果没有锁定数量
        if not locked_seats_num:
            # 为啥返回的是空字典
            return Code.seat_lock_failed, {}
            # 定义了一个create方法,创造订单
            # play.cid影院的排期,排期id,座位id
        order = Order.create(play.cid, pid, sid)
        order.seller_order_no = orderno
        # OrderStatus 是自定义的方法,锁定的值为1
        order.status = OrderStatus.locked.value
        # 订单的票数 = 自定义的 lock方法的返回值 是那个操作数
        order.ticket_num = locked_seats_num
        # 这个save 是自定义了一个类,然后多继承
        order.save()
        return {'locked_seats_num': locked_seats_num}

    @Validator(pid=int, sid=multi_int, orderno=str)
    @route('/unlock/', methods=['POST'])
    def unlock(self):
        pid = request.params['pid']
        sid = request.params['sid']

        # price = request.params['price']
        orderno = request.params['orderno']
        # 获取到场次
        play = Play.get(pid)
        if not play:
            return Code.play_does_not_exist, request.params

        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, request.params
        unlockted_seats_num = PlaySeat.unlock(orderno, pid, sid)
        if not unlockted_seats_num:
            return Code.seat_unlock_failed, {}
        order.status = OrderStatus.unlocked.value
        order.save()
        return {'unlock_seats_num': unlockted_seats_num}

    # 1,200,5000|2,200,5000 传过来的数据是这样
    @Validator(seats=multi_complex_int, orderno=str)
    @route('/buy/', methods=['POST'])
    def buy(self):
        seats = request.params['seats']
        orderno = request.params['orderno']
        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, request.params
        if order.status != OrderStatus.locked.value:
            return Code.order_status_error, {
                'orderno': orderno,
                'status': order.status,
            }

        order.seller_order_no = request.params['orderno']
        order.amount = order.amount or 0
        sid_list = []
        for sid, handle_fee, price in seats:
            sid_list.append(sid)
            order.amount += handle_fee + price
        bought_seats_num = PlaySeat.buy(orderno, order.pid, sid_list)
        if not bought_seats_num:
            return Code.seat_buy_failed, {}
        order.ticket_num = len(seats)
        order.paid_time = datetime.now()
        order.status = OrderStatus.paid.value
        order.gen_ticket_flag()
        order.save()
        return {'bought_seats_num': bought_seats_num,
                'ticket_flag': order.ticket_flag,
                }
