# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from email import message
from marshmallow import Schema, EXCLUDE, RAISE, fields
from lib import ObjectIdField, DatetimeField
    
class RoyaltyNFTRequestParams(Schema):
    class Meta:
        unknown = EXCLUDE
        
    address = fields.String(required=True)
