# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from models import PreLaunchNftWhitelist
from pydash import get
import pydash as py_

from lib import dt_utcnow

class WhitelistHelper:

    @staticmethod
    def checking(formdata):
        _collection = py_.get(formdata, 'collection').lower()
        _address = py_.get(formdata, 'address').lower()
        _check = PreLaunchNftWhitelist.find_one(filter={
            'collection': _collection,
            'address': _address
        })
        return {
            "is_valid_whitelist": _check != None
        }
    