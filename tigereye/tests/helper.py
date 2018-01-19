from unittest import TestCase
from urllib.parse import urlencode

from flask import json
import tigereye
from tigereye.configs.test import Testconfig
from tigereye.helper.code import Code

# 定义了一个测试初始类
class FlaskTestCase(TestCase):
    def setUp(self):
        app = tigereye.create_app(Testconfig)
        # 关掉日志
        app.logger.disabled = True
        # 不用 启动服务也可以利用http协议
        self.app = app.test_client()
        # 这句和** with open() as f一样，是Python提供的语法糖，可以为提供上下文环境省略简化一部分工作。
        # 这里就简化了其压栈和出栈操作，请求线程创建时，Flask会创建应用上下文对象，
        # 并将其压入flask._app_ctx_stack**的栈中，然后在线程退出前将其从栈里弹出。
        with app.app_context():
            from tigereye.models import db
            from tigereye.models.cinema import Cinema
            from tigereye.models.hall import Hall
            from tigereye.models.movie import Movie
            from tigereye.models.play import Play
            from tigereye.models.seat import Seat
            from tigereye.models.order import Order
            from tigereye.helper.code import Code
            db.create_all()
            Cinema.create_test_data(cinema_num=1, hall_num=3, play_num=3)
            Movie.create_test_data()

            # uri 域名后面那段
            # 简化 接口测试方法

    def assert_get(self, uri, assertcode=200, method='GET', **params):
        if method == 'POST':
            rv = self.app.post(uri, data=params)
        else:
            if params:
                rv = self.app.get('%s?%s' % (uri, urlencode(params)))
            else:
                rv = self.app.get(uri)
        print('$'*80)
        print(rv)
        print('$' * 80)
        print(rv.status_code)
        print('$' * 80)
        self.assertEquals(rv.status_code, assertcode)
        return rv



    def get200(self, uri, method='GET', **params):
        return self.assert_get(uri, 200, method, **params)

    def get_json(self, uri, method='GET', **params):
        rv = self.get200(uri, method, **params)
        return json.loads(rv.data)

    # 成功获取到json数据
    def get_succ_json(self, uri, method='GET', **params):
        data = self.get_json(uri, method, **params)
        self.assertEqual(data['rc'], Code.succ.value)
        print(3)
        print(data)
        return data
