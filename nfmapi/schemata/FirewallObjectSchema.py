from marshmallow import fields, Schema

from app import ma
from nfmapi.models import FirewallObject

class FirewallObjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FirewallObject
        ordered = True
    
    uuid = fields.UUID(required=True, description="Unique Identifier", dump_only=True)
    name = fields.String(required=True, description="Firewall name")
    description = fields.String(required=False, description="Description")
    primary_address = fields.String(required=True, description="Primary IP address")
    additional_addresses = fields.List(fields.String(), required=False, description="Additional IP addresses")
    ctime = fields.DateTime(required=True, description="Creation time", dump_only=True)
    mtime = fields.DateTime(required=True, description="Modification time", dump_only=True)