from marshmallow import fields, Schema

from app import ma
from nfmapi.models import NatRule

class NatRuleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NatRule
        ordered = True
    
    uuid = fields.UUID(required=True, description="Unique Identifier", dump_only=True)
    name = fields.String(required=True, description="Rule name")
    description = fields.String(required=False, description="Description")
    source = fields.String(required=False, description="Source object UUID")
    destination = fields.String(required=False, description="Destination object UUID")
    service = fields.String(required=False, description="Service UUID")
    target = fields.String(required=True, description="Target address to which to NAT")
    type = fields.String(required=True, description="Type of NAT (hide, dnat, snat)")
    ctime = fields.DateTime(required=True, description="Creation time", dump_only=True)
    mtime = fields.DateTime(required=True, description="Modification time", dump_only=True)