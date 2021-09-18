from nfmapi.models import NatRule
from nfmapi.schemata import NatRuleSchema
from marshmallow.exceptions import ValidationError
from .BaseResource import BaseResource
from flask import request
from app import db
from uuid import uuid4

path = 'nat_rules'
endpoint = 'nat_rules'


class NatRuleCollectionResource(BaseResource):
    def get(self):
        """List Nat Rules
        ---
        description: List all nat rules
        tags:
          - Nat Rules
        responses:
          200:
            content:
              application/json:
                schema: 
                  type: array
                  items: NatRuleSchema
        """
        objects = NatRule.query.all()
        schema = NatRuleSchema(many = True)
        return schema.dump(objects)

    def post(self):
        """Create nat rule
        ---
        description: Create a nat rule
        tags:
          - Nat Rules
        requestBody:
          content:
            application/json:
              schema: NatRuleSchema
        responses:
          201:
            description: Created
            content:
              application/json:
                schema: NatRuleSchema
          422:
            description: Unprocessable Entity
            content:
              application/json:
                schema: MessageSchema
        """
        json_data = request.get_json()
        try:
            data = NatRuleSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        

        try:
            data["source"]
        except KeyError:
            data["source"] = None
        try:
            data["destination"]
        except KeyError:
            data["destination"] = None
        try:
            data["service"]
        except KeyError:
            data["service"] = None
        
        if not data['source'] and not data['destination']:
            return {"messages": ["Must specify source or destination"]}, 422

        object = NatRule()
        error = False
        messages = []
        for key in data:
            try:
                setattr(object, key, data[key])
            except ValueError as e:
                error = True
                messages.append(e.args[0])
        if error:
            return {"messages": messages}, 422
        db.session.add(object)
        db.session.commit()
        db.session.refresh(object)
        return NatRuleSchema().dump(object)