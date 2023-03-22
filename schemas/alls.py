# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields



class Item(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    name = fields.String()
    price = fields.Float()
    image = fields.String()
    rarity = fields.String()
    total_supply = fields.Int()
    address = fields.String()


class AllsItemResponse(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    
    items = fields.List(fields.Nested(Item), default=[], missing=[])
    num_of_page = fields.Int(default=0, missing=0)
    page_size = fields.Int(default=0, missing=0)
    page = fields.Int(default=0, missing=0)


class AllsItemRequestParams(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    
    chain = fields.String(allow_none=True, default='BSC')
    category = fields.String(allow_none=True, default='Character')
    page = fields.Int(default=1, missing=1)
    page_size = fields.Int(default=10, missing=10)