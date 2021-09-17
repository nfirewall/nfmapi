from app import db, ma
from uuid import uuid4
from datetime import datetime

class FilterRule(db.Model):
    uuid = db.Column(db.String(32), primary_key=True, default=str(uuid4()))
    name = db.Column(db.String(250))
    description = db.Column(db.Text(), nullable=True)
    source = db.Column(db.Text(), nullable=True)
    destination = db.Column(db.Text(), nullable=True)
    service = db.Column(db.Text(), nullable=True)
    action = db.Column(db.String(10))
    ctime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    mtime = db.Column(db.DateTime, onupdate=datetime.utcnow)