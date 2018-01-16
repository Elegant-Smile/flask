from flask import jsonify
from flask_classy import FlaskView
from tigereye.models.movie import Movie


# class MovieView(FlaskView):
#     def all(self):
#         movies = Movie.query.all()
#         print(movies)
#         data_list = []
#         for m in movies:
#             data = {}
#
#             data['name'] = m.name
#             data['halls'] = m.halls
#             data['cid'] = m.cid
#             data['address'] = m.address
#
#             data_list.append(data)
#         return jsonify(data_list)
#仔细比较这一版和上一版本的区别,精髓就在这里了
class MovieView():
    def all(self):
        movies = Movie.query.all()
        print(movies)
        return jsonify(movies)
