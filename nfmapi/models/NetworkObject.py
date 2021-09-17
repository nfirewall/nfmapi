from app import db
from uuid import uuid4
from datetime import datetime
from ipaddress import ip_network
from sqlalchemy.orm import validates

class NetworkObject(db.Model):
    uuid = db.Column(db.String(32), primary_key=True, default=str(uuid4()))
    name = db.Column(db.String(250))
    description = db.Column(db.Text(), nullable=True)
    ipv4 = db.Column(db.String(19), nullable=True)
    ipv6 = db.Column(db.String(43), nullable=True)
    ctime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    mtime = db.Column(db.DateTime, onupdate=datetime.utcnow)

    @validates('ipv4')
    def validate_ipv4(self, key, value):
        if value is None:
            return value
        try:
            ip_network(value)
        except ValueError:
            raise ValueError("Invalid IPv4 address")
        return value
        
    @validates('ipv6')
    def validate_ipv6(self, key, value):
        if value is None:
            return value
        try:
            ip_network(value)
        except ValueError:
            raise ValueError("Invalid IPv6 address")
        return value
        
    @validates('name')
    def validate_name(self, key, value):
        from .HostObject import HostObject
        from .GroupObject import GroupObject
        host = HostObject.query.filter_by(name=value).first()
        network = NetworkObject.query.filter_by(name=value).first()
        group = GroupObject.query.filter_by(name=value).first()
        if host or network or group:
            raise ValueError("Name must be unique")
        return value