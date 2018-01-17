from tigereye.models import db, Model


# 电影
#     id
#     名字
#     语言
#     字幕
#     上映时间
#     版本（2d/3d/4d)
#     模式
#     屏幕尺寸
#     简介
#     状态

class Movie(db.Model, Model):
    mid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    language = db.Column(db.String(32))
    subtitle = db.Column(db.String(32))
    show_date = db.Column(db.Date)
    vision = db.Column(db.String(16))
    model = db.Column(db.String(16))
    screen_size = db.Column(db.String(16))
    introduction = db.Column(db.Text)
    status = db.Column(db.Integer, default=0, index=True, nullable=False)

    def __json__(self):
        keys = vars(self).keys()
        data = {}
        for key in keys:
            if not key.startswith('_'):
                data[key] = getattr(self, key)
        return data

    @classmethod
    def create_test_data(cls, num=10):
        for i in range(1, num + 1):
            m = Movie()
            m.mid = i
            m.sn = str(i).zfill(10)
            m.name = '电影名称%s' % i
            m.language = '英文'
            m.subtitle = '中文'
            # m.show_date =
            m.mode = '数字'
            m.vision = '2D'
            m.screen_size = 'IMAX'
            m.introduction = 'blahblah哈哈'
            m.status = 1
            db.session.add(m)
        db.session.commit()
        print('movie test data done!')
