from . import db
from sqlalchemy.orm import column_property
from sqlalchemy.sql import func


class Actuals(db.Model):
    __tablename__ = "actuals"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ts = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False)

    date = column_property(func.to_char(ts, "YYYY-MM-DD HH24:MI:SS.MS"))

    def __repr__(self):
        return '{{"id": "{}","date": "{}","value": "{}"}}'.format(
            self.id, self.date, self.value
        )

    def __init__(self, value):
        self.value = value
