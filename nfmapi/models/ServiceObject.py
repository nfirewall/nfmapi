from app import db
from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import validates

class ServiceObject(db.Model):
    uuid = db.Column(db.String(32), primary_key=True, default=str(uuid4()))
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    protocol = db.Column(db.String(3), nullable=False)
    dport_low = db.Column(db.Integer(), nullable=False)
    dport_high = db.Column(db.Integer(), nullable=False)
    sport = db.Column(db.Integer(), nullable=True)
    ctime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    mtime = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    @property
    def dport(self) -> str:
        if self.dport_low == self.dport_high:
            return self.dport_low
        return "{}-{}".format(self.dport_low, self.dport_high)
        
    @dport.setter
    def dport(self, value: str):
        print(value)
        split = value.find("-")
        if split > -1:
            low = int(value[:split])
            high = int(value[split+1:])
        else:
            low = high = int(value)
        print(low)
        print(high)
        if low < 1 or low > 65535 or high < 1 or high > 65535:
            raise ValueError("Port/range must be between 1 and 65535")
        self.dport_low = low
        self.dport_high = high

    @validates('name')
    def validate_name(self, key, value):
        from .GroupObject import GroupObject
        group = GroupObject.query.filter_by(name=value).first()
        service = ServiceObject.query.filter_by(name=value).first()
        if group or service:
            raise ValueError("Name must be unique")
        return value
        
    @validates('protocol')
    def validate_protocol(self, key, value):
        if value not in ['tcp', 'udp']:
            raise ValueError("Invalid protocol: {}".format(value))
        return value