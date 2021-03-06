from marshmallow import fields, validate

from app import ma
from nfmanagementapi.models import FilterRule

class FilterRuleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FilterRule
        ordered = True
    
    uuid = fields.UUID(required=True, description="Unique Identifier", dump_only=True)
    name = fields.String(required=True, description="Rule name")
    description = fields.String(required=False, description="Description")
    source = fields.List(fields.UUID(), required=False, description="list of Source object UUIDs")
    destination = fields.List(fields.UUID(), required=False, description="list of Destination object UUIDs")
    service = fields.List(fields.UUID(), required=False, description="list of Service UUIDs")
    action = fields.String(required=True, description="Action to apply", validate=validate.OneOf(["accept", "drop"]))
    ctime = fields.DateTime(required=True, description="Creation time", dump_only=True)
    mtime = fields.DateTime(required=True, description="Modification time", dump_only=True)