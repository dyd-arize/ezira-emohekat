from . import db
from sqlalchemy.orm import column_property
from sqlalchemy.sql import func


class Actuals(db.Model):
    __tablename__ = "actuals"

    ts = db.Column(db.DateTime, primary_key=True)
    value = db.Column(db.Float, nullable=False)

    date = column_property(func.to_char(ts, "YYYY-MM-DD HH24:MI:SS.MS"))

    def __repr__(self):
        return '{{"date": "{}","value": "{}"}}'.format(self.date, self.value)

    def __init__(self, ts, value):
        self.ts = ts
        self.value = value
