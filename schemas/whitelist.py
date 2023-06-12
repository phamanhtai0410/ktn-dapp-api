# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from email import message
from marshmallow import Schema, EXCLUDE, RAISE, fields
    
class WhitelistCheckingBody(Schema):
    class Meta:
        unknown = EXCLUDE
        
    address = fields.String(required=True)

