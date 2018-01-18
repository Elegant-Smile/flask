import functools

from flask import request, jsonify

from tigereye.helper.code import Code

# 为什么要用类,是为了传参数
class Validator(object):
    def __init__(self, **parameter_template):
        self.pt = parameter_template
        # pt是字典

    # 当你创建完一个对象,会调用这个call函数
    def __call__(self, f):
        # functools.wraps 则可以将原函数对象的指定属性复制给包装函数对象,
        @functools.wraps(f)
        def decoreted_function(*args, **kwargs):
            try:
                request.params = {}
                #  items()返回可遍历的(键, 值) 元组数组。
                # k,v = cid=int
                for k, v in self.pt.items():
                    # request.values 这个是字符串那个类似cid=1,是字典
                    request.params[k] = v(request.values[k])
            except Exception:
                response = jsonify(
                    rc=Code.required_parameter_missing.value,
                    msg=Code.required_parameter_missing.name,
                    data={'require_params': k}
                )
                # 含义是你访问的页面域名不存在或者请求错误。
                response.status_code = 400
                return response
            return f(*args, **kwargs)

        return decoreted_function


# sperator=','这样是为了不管是逗号,还是什么符号,都能被切割
def multi_int(values, sperator=','):
    return [int(i) for i in values.split(sperator)]
