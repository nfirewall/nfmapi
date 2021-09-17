from app import db, ma
from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import validates

class ServiceGroupObject(db.Model):
    uuid = db.Column(db.String(32), primary_key=True, default=str(uuid4()))
    name = db.Column(db.String(250))
    description = db.Column(db.Text(), nullable=True)
    children = db.Column(db.PickleType())
    ctime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    mtime = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    @validates('name')
    def validate_name(self, key, value):
        from .ServiceObject import ServiceObject
        service = ServiceObject.query.filter_by(name=value).first()
        group = ServiceGroupObject.query.filter_by(name=value).first()
        if service or group:
            raise ValueError("Name must be unique")
        return value