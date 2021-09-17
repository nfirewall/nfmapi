from app import db, ma
from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import validates
import json
from sqlalchemy import event

class FilterRule(db.Model):
    uuid = db.Column(db.String(32), primary_key=True, default=str(uuid4()))
    name = db.Column(db.String(250), unique=True)
    description = db.Column(db.Text(), nullable=True)
    source = db.Column(db.PickleType(), nullable=True)
    destination = db.Column(db.PickleType(), nullable=True)
    service = db.Column(db.PickleType(), nullable=True)
    action = db.Column(db.String(10), nullable=False)
    ctime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    mtime = db.Column(db.DateTime, onupdate=datetime.utcnow)

    @validates('action')
    def validate_action(self, key, value):
        if not value in ["accept", "drop"]:
            raise ValueError("Invalid action {}".format(value))
        
        return value

    @validates('source')
    def validate_source(self, key, value):
        if value is None:
            return value
        from .HostObject import HostObject
        from .NetworkObject import NetworkObject
        from .NetworkGroupObject import NetworkGroupObject
        
        for item in value:
            host = HostObject.query.filter_by(uuid=item).first()
            network = NetworkObject.query.filter_by(uuid=item).first()
            group = NetworkGroupObject.query.filter_by(uuid=item).first()
            if host is None and network is None and group is None:
                raise ValueError("Invalid source: {}".format(item))
            
        return value
        
    @validates('destination')
    def validate_destination(self, key, value):
        if value is None:
            return value
        from .HostObject import HostObject
        from .NetworkObject import NetworkObject
        from .NetworkGroupObject import NetworkGroupObject
        
        for item in value:
            host = HostObject.query.filter_by(uuid=item).first()
            network = NetworkObject.query.filter_by(uuid=item).first()
            group = NetworkGroupObject.query.filter_by(uuid=item).first()
            if host is None and network is None and group is None:
                raise ValueError("Invalid destination: {}".format(item))
        
        return value
        
    @validates('service')
    def validate_service(self, key, value):
        if value is None:
            return value
        from .ServiceObject import ServiceObject
        from .ServiceGroupObject import ServiceGroupObject
        
        for item in value:
            service = ServiceObject.query.filter_by(uuid=item).first()
            group = ServiceGroupObject.query.filter_by(uuid=item).first()
            if service is None and group is None:
                raise ValueError("Invalid service: {}".format(item))
        
        return value