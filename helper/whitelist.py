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
        _address = py_.get(formdata, 'address').lower()
        _check = PreLaunchNftWhitelist.find_one(filter={
            'address': _address
        })
        return {
            "is_valid_whitelist": _check != None
        }
    