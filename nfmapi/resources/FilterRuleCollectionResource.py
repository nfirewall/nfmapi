from nfmapi.models import FilterRule
from nfmapi.schemata import FilterRuleSchema
from marshmallow.exceptions import ValidationError
from .BaseResource import BaseResource
from flask import request
from app import db
from uuid import uuid4

path = 'filter_rules'
endpoint = 'filter_rules'


class FilterRuleCollectionResource(BaseResource):
    def get(self):
        """List Filter Rules
        ---
        description: List all filter rules
        tags:
          - Filter Rules
        responses:
          200:
            content:
              application/json:
                schema: 
                  type: array
                  items: FilterRuleSchema
        """
        objects = FilterRule.query.all()
        schema = FilterRuleSchema(many = True)
        return schema.dump(objects)

    def post(self):
        """Create filter rule
        ---
        description: Create a filter rule
        tags:
          - Filter Rules
        requestBody:
          content:
            application/json:
              schema: FilterRuleSchema
        responses:
          201:
            description: Created
            content:
              application/json:
                schema: FilterRuleSchema
          422:
            description: Unprocessable Entity
            content:
              application/json:
                schema: MessageSchema
        """
        json_data = request.get_json()
        try:
            data = FilterRuleSchema().load(json_data)
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
        

        object = FilterRule()
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
        return FilterRuleSchema().dump(object)