# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from email import message
from marshmallow import Schema, EXCLUDE, RAISE, fields
from lib import ObjectIdField, DatetimeField

class UserResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    message = fields.String(default='', missing='')
    address = fields.String(default='', missing='')
    nonce = fields.Int(default='', missing='')


class UserResponseLogSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    result = fields.String(default='', missing='')
    address = fields.String(default='', missing='')

class UserInputSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    # code = fields.String(required=True)
    address = fields.String(required=True)
    # sign_message = fields.String(required=True)
    signature = fields.String(required=True)
    nonce = fields.Int(required=True)

class UserRequestParams(Schema):
    class Meta:
        unknown = EXCLUDE
        
    address = fields.String(default='', missing='')
    signature = fields.String(default='', missing='')
    
class UserInfoRequestParams(Schema):
    class Meta:
        unknown = EXCLUDE
        
    address = fields.String(required=True)
    
class UserInfoResponseParams(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField()
    address = fields.String(default='', missing='')
    total_points =fields.Float(default=0, missing=0)
    created_time = DatetimeField(default=0, missing=0)