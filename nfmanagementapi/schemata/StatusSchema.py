from marshmallow import fields, Schema

class StatusSchema(Schema):
    status = fields.String(description='Status')
    version = fields.String(description='Version')