from marshmallow import fields, Schema

from app import ma
from nfmanagementapi.models import NetworkObject

class NetworkObjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NetworkObject
        ordered = True
    
    uuid = fields.UUID(required=True, description="Unique Identifier", dump_only=True)
    name = fields.String(required=True, description="Object name")
    description = fields.String(required=False, description="Description of the object")
    ipv4 = fields.String(required=False, description="IPv4 address of the network")
    ipv6 = fields.String(required=False, description="IPv6 address of the network")
    ctime = fields.DateTime(required=True, description="Creation time of the object", dump_only=True)
    mtime = fields.DateTime(required=True, description="Modification time of the object", dump_only=True)