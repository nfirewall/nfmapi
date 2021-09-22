from app import db
from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import validates

class NatRule(db.Model):
    uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(250), unique=True)
    description = db.Column(db.Text(), nullable=True)
    source = db.Column(db.String(36), nullable=True)
    destination = db.Column(db.String(36), nullable=True)
    service = db.Column(db.String(36), nullable=True)
    target = db.Column(db.String(36))
    type = db.Column(db.String(10))
    ctime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    mtime = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    
    @validates('source')
    def validate_source(self, key, value):
        if value is None:
            return value
        from .HostObject import HostObject
        from .NetworkObject import NetworkObject
        from .NetworkGroupObject import NetworkGroupObject
        
        host = HostObject.query.filter_by(uuid=value).first()
        network = NetworkObject.query.filter_by(uuid=value).first()
        group = NetworkGroupObject.query.filter_by(uuid=value).first()
        if host is None and network is None and group is None:
            raise ValueError("Invalid source: {}".format(value))
            
        return value
        
    @validates('destination')
    def validate_destination(self, key, value):
        if value is None:
            return value
        from .HostObject import HostObject
        from .NetworkObject import NetworkObject
        from .NetworkGroupObject import NetworkGroupObject
        
        host = HostObject.query.filter_by(uuid=value).first()
        network = NetworkObject.query.filter_by(uuid=value).first()
        group = NetworkGroupObject.query.filter_by(uuid=value).first()
        if host is None and network is None and group is None:
            raise ValueError("Invalid source: {}".format(value))
        
        return value
        
    @validates('target')
    def validate_target(self, key, value):
        if value is None:
            return value
        from .HostObject import HostObject
        from .NetworkObject import NetworkObject
        
        host = HostObject.query.filter_by(uuid=value).first()
        network = NetworkObject.query.filter_by(uuid=value).first()
        if host is None and network is None:
            raise ValueError("Invalid source: {}".format(value))
        
        return value
        
    @validates('service')
    def validate_service(self, key, value):
        if value is None:
            return value
        from .ServiceObject import ServiceObject
        from .ServiceGroupObject import ServiceGroupObject
        
        service = ServiceObject.query.filter_by(uuid=value).first()
        group = ServiceGroupObject.query.filter_by(uuid=value).first()
        if service is None and group is None:
            raise ValueError("Invalid service: {}".format(value))
        
        return value
        
    @validates('type')
    def validate_type(self, key, value):
        if value in ['hide', 'snat', 'dnat']:
            return value
        raise ValueError("Invalid NAT type: {}".format(value))