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
from schemas.alls import AllsItemRequestParams, AllsItemResponse, OneItemRequestParams, \
    OneItemResponse, UpcomingRequestParams, UpcommingItemsResponse, ChainSupportResponse, \
    EmailSubscribeRequestParams
from helper.alls import AllsItemHelper
from lib import CHAINS_NAME


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
    

class UpcomingResource(Resource):
    @security.http(
        params=UpcomingRequestParams(),
        response=UpcommingItemsResponse()
    )
    def get(self, params):
        return AllsItemHelper.get_by_filter(params=params)
    

class ChainsSupportResource(Resource):
    
    @security.http(
        response=ChainSupportResponse()
    )
    def get(self):
        _chainsSupport = ChainSupportResponse()
        _res = _chainsSupport.load(data={"items": CHAINS_NAME})
        return _res
    


class EmailSubscribeResource(Resource):
    
    security.http(
        # response=ReferralResponseSchema(),
        params=EmailSubscribeRequestParams()
    )
    def get(self, params):
        _address = py_.get(params, 'address')
        return _address

    @security.http(
        form_data=EmailSubscribeRequestParams()
    )
    def post(self, form_data):
        _email = py_.get(form_data, 'email')
        
        return {}

