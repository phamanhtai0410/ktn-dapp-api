# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from email import message
from marshmallow import Schema, EXCLUDE, RAISE, fields


class UserResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    message = fields.String(default='', missing='')
    address = fields.String(default='', missing='')

class UserInputSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    # code = fields.String(required=True)
    address = fields.String(required=True)
    # sign_message = fields.String(required=True)
    signature = fields.String(required=True)
    message = fields.String(required=True)

class UserRequestParams(Schema):
    class Meta:
        unknown = EXCLUDE
        
    address = fields.String(default='', missing='')
    signature = fields.String(default='', missing='')