# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, RAISE, fields

from constants import Constants


class LeaderBoardItem(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    address = fields.String()
    event = fields.String()
    point = fields.Int()
    rank = fields.Int()

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
    event = fields.String(default=Constants.TOP_REFERRAL_EVENT_NAME, missing=Constants.TOP_REFERRAL_EVENT_NAME)
    page = fields.Int(default=1, missing=1)
    page_size = fields.Int(default=10, missing=10)