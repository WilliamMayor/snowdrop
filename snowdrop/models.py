import datetime

from flask.ext.sqlalchemy import SQLAlchemy

from . import app

db = SQLAlchemy(app)


class Archive(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String)
    name = db.Column(db.String)
    date = db.Column(db.Date, default=datetime.date.today)
    size = db.Column(db.Integer)
    upload_progress = db.Column(db.Integer)
