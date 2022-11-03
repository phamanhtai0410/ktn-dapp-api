# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from email import message
from marshmallow import Schema, EXCLUDE, RAISE, fields
from lib import ObjectIdField, DatetimeField
    
class PaymentRequestParams(Schema):
    class Meta:
        unknown = EXCLUDE
        
    chain_id = fields.Integer(required=False)
    
class PaymentResponseParams(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField()
    asset = fields.String(default='', missing='')
    asset_address = fields.String(default='', missing='')
    chain =fields.String(default='', missing='')
    chain_id = fields.Integer(default=0, missing=0)
    asset_logo = fields.String(default='', missing='')
    chain_logo = fields.String(default='', missing='')
    is_active = fields.Boolean(default=False, missing= False)
    created_time = DatetimeField(default='', missing='')
    
class PaymentListResponseParams(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    
    assets = fields.List(fields.Nested(PaymentResponseParams), default=[], missing=[])