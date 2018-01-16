from flask_classy import FlaskView, route


# misc杂项,乱七八遭的放一起
class MiscView(FlaskView):
    # 本来是类名加方法名,组成了你的url
    # 配置根目录,这样不用写 miscview
    route_base = '/'

    # 根目录,index方法是类的系统默认根方法
    def index(self):
        return self.check()

    def check(self):
        return 'i am ok '
