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
# 仔细比较这一版和上一版本的区别,精髓就在这里了

class MovieView(FlaskView):
    def all(self):
        movies = Movie.query.all()
        print(movies)
        # jsonify 会把字典,列表,元祖 转为字符串,然后flask会自动调用make_response 对象返回过去
        # 但是我们输出的是 对象,对象,jesonencoder系统编码不了,所以我们重写了JSONEncoder方法,加了一个判断
        # 如果是对象,我们就把他转为字典,其他的跟着系统走

        # *args没有key值， ** kwargs有key值,*args可以当作可容纳多个变量组成的list或tuple
        # **kwargs可以当作容纳多个key和value的dictionary
        return jsonify(movies)
