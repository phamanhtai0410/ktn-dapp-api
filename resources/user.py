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


from schemas.user import UserRequestParams, UserResponseSchema, UserInputSchema
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
        params=UserInputSchema(),
        response=UserResponseSchema()
    )
    
    def post(self, params):
        _address = py_.get(params, 'address')
        _signature = py_.get(params, 'signature')
        _message = py_.get(params,'message')
        res  = UserHelper.verify_signature(_address,_message ,_signature )
        return res
