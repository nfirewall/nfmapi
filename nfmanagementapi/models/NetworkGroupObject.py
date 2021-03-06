from app import db, ma
from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import validates

class NetworkGroupObject(db.Model):
    uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(250))
    description = db.Column(db.Text(), nullable=True)
    children = db.Column(db.PickleType())
    ctime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    mtime = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    @validates('name')
    def validate_name(self, key, value):
        from .HostObject import HostObject
        from .NetworkObject import NetworkObject
        host = HostObject.query.filter_by(name=value).first()
        network = NetworkObject.query.filter_by(name=value).first()
        group = NetworkGroupObject.query.filter_by(name=value).first()
        if host or network or group:
            raise ValueError("Name must be unique")
        return value
    
    @validates('children')
    def validate_children(self, key, value):
        from .HostObject import HostObject
        from .NetworkObject import NetworkObject
        for child in value:
            host = HostObject.query.filter_by(uuid=child).first()
            network = NetworkObject.query.filter_by(uuid=child).first()
            group = NetworkGroupObject.query.filter_by(uuid=child).first()
            if host or network or group:
                return value
            raise ValueError("Object not found: {}".format(value))
            