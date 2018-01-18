
from tigereye.extensions.validator import Validator
from flask import request

from tigereye.api import ApiView
from tigereye.models.seat import PlaySeat, SeatType


class PlayView(ApiView):
    @Validator(pid=int)
    def seat(self):
        pid = request.params['pid']
        return PlaySeat.query.filter(
            PlaySeat.pid == pid,
            PlaySeat.seat_type != SeatType.road.value
        ).all()
