# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource

from connect import security


class IAPIExchangeResource(Resource):

    @security.http()
    def post(self, form_data):
        return {}
