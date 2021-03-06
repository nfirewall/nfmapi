from marshmallow import fields, validate

from app import ma
from nfmanagementapi.models import NatRule

class NatRuleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NatRule
        ordered = True
    
    uuid = fields.UUID(required=True, description="Unique Identifier", dump_only=True)
    name = fields.String(required=True, description="Rule name")
    description = fields.String(required=False, description="Description")
    source = fields.UUID(required=False, description="Source object UUID")
    destination = fields.UUID(required=False, description="Destination object UUID")
    service = fields.UUID(required=False, description="Service UUID")
    target = fields.String(required=True, description="Target address to which to NAT")
    type = fields.String(required=True, description="Type of NAT", validate=validate.OneOf(["hide", "dnat", "snat"]))
    ctime = fields.DateTime(required=True, description="Creation time", dump_only=True)
    mtime = fields.DateTime(required=True, description="Modification time", dump_only=True)