from datetime import datetime

from . import db

class Todo(db.Model):
    id = db.Column(db.UUID, primary_key=True)
    code = db.Column(db.Integer)
    title = db.Column(db.String(100))
    complete = db.Column(db.String(1), default='n')
    date_added = db.Column(db.DateTime, default=datetime.now)