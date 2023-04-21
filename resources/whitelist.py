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
from schemas.whitelist import WhitelistCheckingBody
from helper.whitelist import WhitelistHelper


class WhitelistCheckingResource(Resource):

    @security.http(
        form_data=WhitelistCheckingBody()
    )
    def post(self, form_data):
        print("Check whitelist : ", form_data)
        return WhitelistHelper.checking(formdata=form_data)
