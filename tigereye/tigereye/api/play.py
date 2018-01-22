from tigereye.extensions.validator import Validator
from flask import request
import redis
from tigereye.api import ApiView
from tigereye.models.seat import PlaySeat, SeatType
from flask import json

r = redis.Redis()


class PlayView(ApiView):
    # 没有做数据库查询优化的
    # @Validator(pid=int)
    # def seat(self):
    #     return PlaySeat.query.filter(
    #         PlaySeat.pid == request.params['pid'],
    #         PlaySeat.seat_type != SeatType.road.value).all()




    @Validator(pid=int)
    def seat(self):
        pid = request.params['pid']
        key = 'play_seat_%s' % pid
        ps = r.lrange(key, 0, -1)
        ps = [json.loads(p.decode('utf-8')) for p in ps]
        # lrange 返回的是一个列表
        if not ps:
            ps = PlaySeat.query.filter(
                PlaySeat.pid == pid,
                PlaySeat.seat_type != SeatType.road.value
            ).all()
            # print('123')
            r.lpush(key, *[json.dumps(p) for p in ps])  # 从右侧把数据插进去
            # print(ps)
        return ps

