from datetime import datetime
import math

from flask import current_app

from tigereye.models import db, Model
import faker
import random

# 影院
#     id
#     名称
#     地址
#     影厅数量
#     手续费
#     购买数量限制
#     状态
from tigereye.models.seat import PlaySeat


class Cinema(db.Model, Model):
    cid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    address = db.Column(db.String(256), nullable=False)
    halls = db.Column(db.Integer, default=0, nullable=False)
    handle_fee = db.Column(db.Integer, default=0, nullable=False)
    buy_limit = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.Integer, default=0, index=True, nullable=False)

    @classmethod
    # play_num 排期
    def create_test_data(cls, cinema_num=10, hall_num=10, play_num=10):

        from tigereye.models.hall import Hall
        from tigereye.models.movie import Movie
        from tigereye.models.play import Play
        from tigereye.models.seat import Seat
        from tigereye.models.order import Order
        f = faker.Faker('zh_CN')
        screen_types = ['普通', 'IMAX']
        audio_types = ['普通', '杜比环绕']

        for i in range(1, cinema_num + 1):
            cinema = Cinema()
            cinema.cid = i
            cinema.name = '%s 影城' % f.name()
            cinema.address = f.address()
            cinema.status = 1
            cinema.save()

            for n in range(1, hall_num + 1):
                hall = Hall()
                hall.cid = cinema.cid
                hall.name = '%s号厅' % n
                hall.screen_type = random.choice(screen_types)
                # 音效
                hall.audio_type = random.choice(audio_types)

                hall.seats_num = 25
                # 座位状态
                hall.status = 1
                hall.save()

                seats = []
                for s in range(1, hall.seats_num + 1):
                    seat = Seat()
                    seat.cid = cinema.cid
                    seat.hid = hall.hid
                    seat.x = s % 5 or 5
                    seat.y = math.ceil(s / 5)
                    seat.row = seat.x
                    seat.column = seat.y
                    seat.seat_type = 1
                    seat.put()
                    seats.append(seat)
                # 为啥是这个commit,
                Seat.commit()

                for p in range(1, play_num + 1):
                    play = Play()
                    play.cid = cinema.cid
                    play.hid = hall.hid
                    play.mid = p
                    play.start_time = datetime.now()
                    play.duration = 3600
                    play.price_type = 1
                    play.price = 7000
                    play.market_price = 5000
                    play.lowest_price = 3000
                    play.status = 1
                    play.save()

                    for seat in seats:
                        ps = PlaySeat()
                        ps.pid = play.pid
                        ps.copy(seat)
                        ps.put()
                    PlaySeat.commit()
                    # print(' playseat')
        print('create test data done !')#
        current_app.logger.info('create test data done')
