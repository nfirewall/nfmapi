from marshmallow import fields, Schema

class MessageSchema(Schema):
    message = fields.String(description='Response message')