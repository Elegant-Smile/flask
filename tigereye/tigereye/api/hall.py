from flask import jsonify, request
from flask_classy import FlaskView
from tigereye.models.cinema import Cinema
from tigereye.models.hall import Hall
from tigereye.models.seat import Seat
from tigereye.api import ApiView
from tigereye.helper.code import Code


# 获取影厅的所有座位
class HallView(ApiView):
    def seats(self):
        hid = request.args.get('hid')
        hall = Hall.get(hid)
        if not hall:
            # 都是自定了 返回的错误提示,而且返回了输入的参数,而且还是软编码,错误类型会写文档提示
            return Code.hall_does_not_exist, request.args
        hall.seats = Seat.query.filter_by(hid=hid).all()
        return hall
