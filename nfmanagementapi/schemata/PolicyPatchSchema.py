from marshmallow import fields, Schema

from app import ma
from nfmanagementapi.models import Policy

class PolicyPatchSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Policy
        ordered = True
    
    uuid = fields.UUID(required=True, description="Unique Identifier", dump_only=True)
    name = fields.String(required=False, description="Policy name")
    description = fields.String(required=False, description="Description")
    filter_rules = fields.List(fields.UUID(), required=False, description="Rules to apply")
    nat_rules = fields.List(fields.UUID(), required=False, description="Rules to apply")
    targets = fields.List(fields.UUID(), required=False, description="Targets to which to apply the policy")
    ctime = fields.DateTime(required=True, description="Creation time", dump_only=True)
    mtime = fields.DateTime(required=True, description="Modification time", dump_only=True)