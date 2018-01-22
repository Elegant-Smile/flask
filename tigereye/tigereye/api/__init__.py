import functools
import time
from flask import request, Response, make_response, current_app
from flask.json import jsonify
from flask_classy import FlaskView
from tigereye.helper.code import Code


# 自定义类视图,继承了flaskView,对改写
class ApiView(FlaskView):
    # 自定义的方法
    def before_request(self, name, **kwargs):
        self.request_start_time = time.time()
        # print(2)
        # print(self.request_start_time)

    def after_request(self, name, response):
        # current_app 是全局变量
        current_app.logger.info('%s response time :%s' % (request.path, time.time() - self.request_start_time))
        # 请求的路径 以及所花费的时间
        # print(1)
        # print(response)
        return response

    @classmethod
    # 重写这个方法
    def make_proxy_method(cls, name):
        """Creates a proxy function that can be used by Flasks routing. The
        proxy instantiates the FlaskView subclass and calls the appropriate
        method.

        :param name: the name of the method to create a proxy for
        """

        i = cls()
        view = getattr(i, name)

        if cls.decorators:
            for decorator in cls.decorators:
                view = decorator(view)

        @functools.wraps(view)
        def proxy(**forgettable_view_args):
            # Always use the global request object's view_args, because they
            # can be modified by intervening function before an endpoint or
            # wrapper gets called. This matches Flask's behavior.
            del forgettable_view_args

            if hasattr(i, "before_request"):
                response = i.before_request(name, **request.view_args)
                if response is not None:
                    return response

            before_view_name = "before_" + name
            if hasattr(i, before_view_name):
                before_view = getattr(i, before_view_name)
                response = before_view(**request.view_args)
                if response is not None:
                    return response
            # view 就是我们写的函数
            response = view(**request.view_args)

            # 判断是不是一个Response对象
            # isinstance(object, classinfo)
            # 参数  # object -- 实例对象。  # classinfo -- 可以是直接或间接类名、基本类型或者有它们组成的元组
            if not isinstance(response, Response):  # 大写Response, flask默认的返回对象
                # 如果不是,则先获取他的类型
                response_type = type(response)
                # 如果是tuple类型,并且长度大于1,这能证明什么
                if response_type == tuple and len(response) > 1:
                    # tuple 一分为二
                    rc, _data = response
                    response = jsonify(rc=rc.value, msg=rc.name, data=_data)  # jsonify flask默认的对象
                else:
                    # 已经 成功返回
                    # return jsonify(rc=0, msg='succ', data=response)
                    response = jsonify(rc=Code.succ.value, msg=Code.succ.name, data=response)
                    # -----------自定义内容结束----------- #
            # 这是源码
            # if not isinstance(response, Response):
            #     response = make_response(response)

            after_view_name = "after_" + name
            if hasattr(i, after_view_name):
                after_view = getattr(i, after_view_name)
                response = after_view(response)

            if hasattr(i, "after_request"):
                response = i.after_request(name, response)

            return response

        return proxy
