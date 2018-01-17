from flask_script import Manager, Server, Shell
from tigereye.app import create_app
from tigereye.models import db

app = create_app()
manager = Manager(app)

#自定义验证方法
def _make_context():
    from tigereye.models.cinema import Cinema
    from tigereye.models.hall import Hall
    from tigereye.models.movie import Movie
    from tigereye.models.play import Play
    from tigereye.models.seat import Seat
    from tigereye.models.order import Order

    # 把全局变量加到局部变量里,类似于列表的append
    locals().update(globals())
    return dict(**locals())


manager.add_command('runserver', Server('127.0.0.1', port=8000))
manager.add_command('shell', Shell(make_context=_make_context))


# 自定义了一个createdb命令,创建数据库
@manager.command
def createdb():
    # 引入models对象
    from tigereye.models.cinema import Cinema
    from tigereye.models.hall import Hall
    from tigereye.models.movie import Movie
    from tigereye.models.play import Play
    from tigereye.models.seat import Seat
    from tigereye.models.order import Order
    db.create_all()


@manager.command
def dropdb():
    from tigereye.models.cinema import Cinema
    from tigereye.models.hall import Hall
    from tigereye.models.movie import Movie
    from tigereye.models.play import Play
    from tigereye.models.seat import Seat
    from tigereye.models.order import Order
    db.drop_all()

@manager.command
def init():
    dropdb()
    createdb()
    testdata()

@manager.command
def testdata():
    from tigereye.models.cinema import Cinema
    from tigereye.models.movie import Movie
    Cinema.create_test_data()
    Movie.create_test_data()

if __name__ == '__main__':
    manager.run()
