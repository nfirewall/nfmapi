from marshmallow import fields, Schema

from app import ma
from nfmapi.models import ServiceObject

class ServiceObjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceObject
        ordered = True
        exclude = ("dport_low", "dport_high", "sport")
    
    uuid = fields.UUID(required=True, description="Unique Identifier", dump_only=True)
    name = fields.String(required=True, description="Object name")
    description = fields.String(required=False, description="Description of the object")
    protocol = fields.String(required=True, description="Protocol (tcp/udp)")
    dport = fields.String(required=True, description="Destination Port")
    ctime = fields.DateTime(required=True, description="Creation time of the object", dump_only=True)
    mtime = fields.DateTime(required=True, description="Modification time of the object", dump_only=True)