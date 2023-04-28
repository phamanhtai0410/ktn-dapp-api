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
from exception import InvalidEmail
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
    @security.http(
        form_data=EmailSubscribeRequestParams()
    )
    def post(self, form_data):
        _email = py_.get(form_data, 'email').strip()
        _is_email = AllsItemHelper.check_email_subscirbe(_email)
        if _is_email is False:
            raise InvalidEmail
        AllsItemHelper.update_email_subscirbe(_email)
        return {}
