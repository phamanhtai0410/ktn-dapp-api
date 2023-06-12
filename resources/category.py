from flask_restful import Resource
from connect import security
from helper.category import CategoryHelper
from schemas.category import CollectionCategoryResponse

class CategoryResource(Resource):
    @security.http(
            response=CollectionCategoryResponse()
    )
    def get(self):
        return CategoryHelper.get_all_category()