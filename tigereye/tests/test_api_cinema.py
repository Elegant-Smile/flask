from flask import json

from tigereye.helper.code import Code
from .helper import FlaskTestCase


class TestApiCinema(FlaskTestCase):
    def test_cinema_all(self):
        # response = self.app.get('/cinema/all/')
        # # 断言 如果相等就通过,python自动化测试断言
        # self.assertEquals(response.status_code, 200)
        # # json.loads将已编码的 JSON 字符串解码为 Python 对象
        # # json.dumps	将 Python 对象编码成 JSON 字符串
        # data = json.loads(response.data)
        # print(data)
        # # 最后为啥要判断他两相等 ,这里不等会报错
        # # 这个rc 是validator 里rc=Code.required_parameter_missing.value,可是这个值是100
        # self.assertEquals(data['rc'], Code.succ.value)

        # 这是优化后的代码
        self.get_succ_json('/cinema/all/')

        def test_cinema_halls(self):
            self.assert_get('/cinema/hall/', 400)
            data = self.get_succ_json('/cinema/all')
            self.assertIsNotNone(data['data'])