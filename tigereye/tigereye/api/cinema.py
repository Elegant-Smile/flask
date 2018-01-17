from flask import jsonify, request
from flask_classy import FlaskView
from tigereye.models.cinema import Cinema


class CinemaView(FlaskView):
    def index(self):
        cinemas = Cinema.query.all()
        print(cinemas)
        data_list = []
        for c in cinemas:
            data = {}
            data['name'] = c.name
            data['halls'] = c.halls
            data['cid'] = c.cid
            data['address'] = c.address
            data_list.append(data)
        return jsonify(data_list)

    def get(self):
        cid = request.args['cid']
        cinema = Cinema.get(cid)
        if not cinema:
            return jsonify({'msg': 'Cinema %s not found' % cid})
        return jsonify(cinema)
