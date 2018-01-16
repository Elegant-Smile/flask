from flask_script import Manager, Server
from tigereye.app import create_app
from tigereye.models import db
app = create_app()
manager = Manager(app)
manager.add_command('runserver', Server('127.0.0.1', port=8000))


#自定义了一个createdb命令,创建数据库
@manager.command
def createdb():
    #引入models对象
    from tigereye.models.cinema import  Cinema
    from tigereye.models.hall import  Hall
    from tigereye.models.movie import  Movie
    db.create_all()

if __name__ == '__main__':
    manager.run()
