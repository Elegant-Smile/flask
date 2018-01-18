
from tigereye.extensions.validator import Validator
from flask import jsonify, request
from tigereye.models.cinema import Cinema
from tigereye.models.hall import Hall
from tigereye.api import ApiView
from tigereye.helper.code import Code
from tigereye.models.movie import Movie
from tigereye.models.play import Play


class CinemaView(ApiView):
    def index(self):
        cinemas = Cinema.query.all()
        # print(cinemas)
        return cinemas

    def get(self):
        cid = request.args['cid']
        cinema = Cinema.get(cid)
        if not cinema:
            return Code.cinema_does_not_exist, request.args
        return cinema

    # 获取某家电影院的所有影厅
    @Validator(cid=int)
    def halls(self):
        cid = request.params['cid']
        cinema = Cinema.get(cid)
        if not cinema:
            # return 1, request.args
            return Code.cinema_does_not_exist, request.args
        cinema.halls = Hall.query.filter_by(cid=cid).all()
        return cinema

    @Validator(cid=int)
    def plays(self):
        # 使用Request.Params["id"]来获取参数是一种比较有效的途径。
        cid = request.params['cid']
        cinema = Cinema.get(cid)
        if not cinema:
            return Code.cinema_does_not_exist, request.args
        cinema.plays = Play.query.filter_by(cid=cid).all()
        for play in cinema.plays:
            play.movie = Movie.get(play.mid)

        # 为啥返回的是cinema
        return cinema

