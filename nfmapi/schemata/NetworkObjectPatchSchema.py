from marshmallow import fields, Schema

from app import ma
from nfmapi.models import NetworkObject

class NetworkObjectPatchSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NetworkObject
        ordered = True
    
    uuid = fields.UUID(description="Unique Identifier", dump_only=True)
    name = fields.String(required=False, description="Object name")
    description = fields.String(required=False, description="Description of the object")
    ipv4 = fields.String(required=False, description="IPv4 address of the network")
    ipv6 = fields.String(required=False, description="IPv6 address of the network")
    ctime = fields.DateTime(required=True, description="Creation time of the object", dump_only=True)
    mtime = fields.DateTime(required=True, description="Modification time of the object", dump_only=True)