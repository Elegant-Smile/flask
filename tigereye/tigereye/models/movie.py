from tigereye.models import db


class Movie(db.Model):
    mid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    language = db.Column(db.String(32))
    subtitle = db.Column(db.String(32))
    show_date = db.Column(db.Date)
    vision = db.Column(db.String(16))
    model = db.Column(db.String(16))
    screen_size = db.Column(db.String(16))
    introduction = db.Column(db.Text)
    status = db.Column(db.Integer, nullable=False, default=0, index=True)

    def __jeson__(self):
        keys = vars(self).keys
        data = {}
        for key in keys:
            if not key.startswith('_'):
                data[key] = getattr(self, key)
            return data

    # def __dict__(self):
    #     return self.__jeson__()
