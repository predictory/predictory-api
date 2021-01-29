from db import db


class SettingModel(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))
    name = db.Column(db.String(100))
    value = db.Column(db.String(100))

    def __init__(self, typ, name, value):
        self.type = typ
        self.name = name
        self.value = value
