from app import db
from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import validates

class Policy(db.Model):
    uuid = db.Column(db.String(32), primary_key=True, default=str(uuid4()))
    name = db.Column(db.String(250), unique=True)
    description = db.Column(db.Text(), nullable=True)
    targets =  db.Column(db.PickleType(), nullable=False)
    filter_rules = db.Column(db.PickleType(), nullable=False)
    nat_rules = db.Column(db.PickleType(), nullable=True)
    ctime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    mtime = db.Column(db.DateTime, onupdate=datetime.utcnow)

    
    @validates('targets')
    def validate_targets(self, key, value):
        if value is None:
            return value
        from .FirewallObject import FirewallObject
        
        for item in value:
            firewall = FirewallObject.query.filter_by(uuid=item).first()
            if firewall is None:
                raise ValueError("Invalid target: {}".format(item))
            
        return value
    
    @validates('filter_rules')
    def validate_filter_rules(self, key, value):
        if value is None:
            return value
        from .FilterRule import FilterRule
        
        for item in value:
            filter_rule = FilterRule.query.filter_by(uuid=item).first()
            if filter_rule is None:
                raise ValueError("Invalid filter rule: {}".format(item))
            
        return value
    
    @validates('nat_rules')
    def validate_nat_rules(self, key, value):
        if value is None:
            return value
        from .NatRule import NatRule
        
        for item in value:
            nat_rule = NatRule.query.filter_by(uuid=item).first()
            if nat_rule is None:
                raise ValueError("Invalid filter rule: {}".format(item))
            
        return value