# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields, validate


class EventParam(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(required=True, validate=validate.OneOf(['stake']))


class EventSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    total = fields.Int(missing=0)
