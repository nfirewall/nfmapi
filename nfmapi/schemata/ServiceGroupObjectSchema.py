from marshmallow import fields, Schema

from app import ma
from nfmapi.models import ServiceGroupObject

class ServiceGroupObjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceGroupObject
        ordered = True
    
    uuid = fields.UUID(required=True, description="Unique Identifier", dump_only=True)
    name = fields.String(required=True, description="Object name")
    description = fields.String(required=False, description="Description of the object")
    children = fields.List(fields.String(), required=True, description="UUIDs of children objects")
    ctime = fields.DateTime(required=True, description="Creation time of the object", dump_only=True)
    mtime = fields.DateTime(required=True, description="Modification time of the object", dump_only=True)