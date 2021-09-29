from marshmallow import fields, validate

from app import ma
from nfmanagementapi.models import ServiceObject

class ServiceObjectPatchSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceObject
        ordered = True
        exclude = ("dport_low", "dport_high", "sport")
    
    uuid = fields.UUID(required=True, description="Unique Identifier", dump_only=True)
    name = fields.String(required=False, description="Object name")
    description = fields.String(required=False, description="Description of the object")
    protocol = fields.String(required=False, description="Protocol", validate=validate.OneOf(["tcp", "udp"]))
    dport = fields.String(required=False, description="Destination Port")
    ctime = fields.DateTime(required=True, description="Creation time of the object", dump_only=True)
    mtime = fields.DateTime(required=True, description="Modification time of the object", dump_only=True)