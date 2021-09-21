from app import db
from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import validates

class FirewallObject(db.Model):
    uuid = db.Column(db.String(32), primary_key=True, default=str(uuid4()))
    name = db.Column(db.String(250), unique=True)
    description = db.Column(db.Text(), nullable=True)
    primary_address = db.Column(db.String(32), unique=True, nullable=False)
    additional_addresses = db.Column(db.PickleType(), nullable=True)
    ctime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    mtime = db.Column(db.DateTime, onupdate=datetime.utcnow)