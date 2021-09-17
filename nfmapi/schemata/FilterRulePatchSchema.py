from marshmallow import fields, Schema

from app import ma
from nfmapi.models import FilterRule

class FilterRulePatchSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FilterRule
        ordered = True
    
    uuid = fields.UUID(required=True, description="Unique Identifier", dump_only=True)
    name = fields.String(required=False, description="Rule name")
    description = fields.String(required=False, description="Description")
    source = fields.List(fields.String(), required=False, description="list of Source object UUIDs")
    destination = fields.List(fields.String(), required=False, description="list of Destination object UUIDs")
    service = fields.List(fields.String(), required=False, description="list of Service UUIDs")
    action = fields.List(fields.String(), required=False, description="Action to apply")
    ctime = fields.DateTime(required=True, description="Creation time", dump_only=True)
    mtime = fields.DateTime(required=True, description="Modification time", dump_only=True)