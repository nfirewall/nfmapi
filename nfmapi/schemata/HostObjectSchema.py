from marshmallow import fields, Schema

from app import ma
from nfmapi.models import HostObject

class HostObjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HostObject
        ordered = True
    
    uuid = fields.UUID(required=True, description="Unique Identifier", dump_only=True)
    name = fields.String(required=True, description="Object name")
    description = fields.String(required=False, description="Description of the object")
    ipv4 = fields.String(required=False, description="IPv4 address of the host")
    ipv6 = fields.String(required=False, description="IPv6 address of the host")
    ctime = fields.DateTime(required=True, description="Creation time of the object", dump_only=True)
    mtime = fields.DateTime(required=True, description="Modification time of the object", dump_only=True)