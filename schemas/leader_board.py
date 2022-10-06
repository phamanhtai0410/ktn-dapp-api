# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, RAISE, fields


class LeaderBoardItem(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    public_address = fields.String()
    total_user_linked = fields.Int()

class LeaderBoardResponse(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    
    items = fields.List(fields.Nested(LeaderBoardItem), default=[], missing=[])
    num_of_page = fields.Int(default=0, missing=0)
    page_size = fields.Int(default=0, missing=0)
    page = fields.Int(default=0, missing=0)

class LeaderBoardRequestParams(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    
    search = fields.String(allow_none=True)
    page = fields.Int(default=1, missing=1)
    page_size = fields.Int(default=10, missing=10)