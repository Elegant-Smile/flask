# from flask import json
#
# from tigereye.helper.code import Code
# from tigereye.models.seat import SeatStatus
# from .helper import FlaskTestCase
#
# pid = 1
# sid_list = [1, 2]
# sid = ','.join([str(i) for i in sid_list])
# price = 5000
# orderno = 'test-%s-%s' % (pid, sid)
#
#
# class TestApiSeat(FlaskTestCase):
#     def test_seat1_lock(self):
#         locked_seats_num = len(sid_list)
#         rv = self.get_succ_json('/seat/lock/',
#                                 method='POST',
#                                 orderno=orderno,
#                                 pid=pid,
#                                 sid=sid,
#                                 price=price,)
#         print(rv)
#         self.assertEqual(rv['data']['locked_seats_num'], locked_seats_num)
#
#         # 确定锁定成功,数据写入数据库
#         print(1)
#         rv = self.get_succ_json('/play/seats/', pid=pid)
#         print(2)
#         succ_count = 0
#         for seat in rv['data']:
#             if seat['orderno'] == orderno:
#                 self.assertEqual(seat['status'], SeatStatus.locked.value)
#                 succ_count += 1
#         self.assertEqual(succ_count, locked_seats_num)
#
#         # 确实重复锁定会失败
#         rv = self.get_json('/seat/lock/',
#                            method='POST',
#                            orderno=orderno,
#                            pid=pid,
#                            sid=sid,
#                            price=price,
#                            )
#         print(rv['data'])
#         self.assertEqual(rv['rc'], Code.seat_lock_failed.value)

from flask import json

from tigereye.models.seat import SeatStatus
from .helper import FlaskTestCase
from tigereye.helper.code import Code


pid = 1
sid_list = [1, 2]
sid = ','.join([str(i) for i in sid_list])
price = 5000
orderno = 'test-%s-%s' % (pid, sid)


class TestApiSeat(FlaskTestCase):

    def test_seat1_lock(self):
        locked_seats_num = len(sid_list)
        rv = self.get_succ_json("/seat/lock/",
                                method='POST',
                                orderno=orderno,
                                pid=pid,
                                sid=sid,
                                price=price)
        self.assertEqual(rv['data']['locked_seats_num'], locked_seats_num)
        # 确定锁定成功,数据写入数据库, 这个路径是拼接路径,和你自己的classview 类名＋方法名是一样的
        rv = self.get_succ_json("/play/seat/", pid=pid)
        succ_count = 0
        for seat in rv['data']:
            if seat['orderno'] == orderno:
                self.assertEqual(seat['status'], SeatStatus.locked.value)
                succ_count += 1
        self.assertEqual(succ_count, locked_seats_num)

        # 确定重复锁座会失败
        rv = self.get_json("/seat/lock/",
                                method='POST',
                                orderno=orderno,
                                pid=pid,
                                sid=sid,
                                price=price)
        self.assertEqual(rv['rc'], Code.seat_lock_failed.value)

