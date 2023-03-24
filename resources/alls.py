# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask import request
from flask_restful import Resource
import pydash as py_
from connect import security
from schemas.alls import AllsItemRequestParams, AllsItemResponse, OneItemRequestParams, OneItemResponse
from helper.alls import AllsItemHelper

class AllsItemResource(Resource):

    @security.http(
        params=AllsItemRequestParams(),
        response=AllsItemResponse()
    )
    def get(self, params):
        return AllsItemHelper.get_by_filter(params=params)

class OneItemResource(Resource):
    
    @security.http(
        params=OneItemRequestParams(),
        response=OneItemResponse()
    )
    def get(self, params):
        return AllsItemHelper.get_one_by_filter(params=params)