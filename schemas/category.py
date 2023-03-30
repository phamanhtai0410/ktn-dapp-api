from marshmallow import Schema, EXCLUDE, fields


class Category(Schema):
    class Meta:
        unknown = EXCLUDE
    
    name = fields.Str(allow_none=False)
    code = fields.Str(allow_none=False)
    min_price = fields.Float()
    total_supply = fields.Integer()

class CollectionCategoryResponse(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    categories = fields.List(fields.Nested(Category), default=[], missing=[])
