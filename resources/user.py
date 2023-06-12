# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import requests
from flask import request
from email import message
from flask_restful import Resource
from pydash import get
import pydash as py_
from connect import security


from schemas.user import UserRequestParams, UserResponseSchema, UserInputSchema, UserResponseLogSchema, UserInfoRequestParams, UserInfoResponseParams
from helper import UserHelper


class User(Resource):

    @security.http(
        params=UserRequestParams(),
        response=UserResponseSchema()
    )
    def get(self, params):
        _address = py_.get(params, 'address')
        message = UserHelper.get_sign_message(_address)
        return message
    
    @security.http(
        form_data = UserInputSchema(),
        response= UserResponseLogSchema()
    )
    
    def post(self, form_data):
        _address = py_.get(form_data, 'address')
        _signature = py_.get(form_data, 'signature')
        _nonce = py_.get(form_data,'nonce')
        res  = UserHelper.verify_signature(_address,_nonce ,_signature)
        return res


class UserInfo(Resource):
    @security.http(
        params=UserInfoRequestParams(),
        response=UserInfoResponseParams()
    )
    def get(self, params):
        _address = py_.get(params, 'address')
        res = UserHelper.get_user_info(_address)
        return res