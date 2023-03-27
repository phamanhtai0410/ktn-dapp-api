import string
import random

from pydash import get

import pydash as py_
from models import AdminDefaultConfigsModel


class AdminConfigHelper:
    @staticmethod
    def get():
        _whitelist_mint = AdminDefaultConfigsModel.find({
            'type': 'WHITE_LIST_MINT'
        }, cache=True, hset_field='name')
        _whitelist_start_time = py_.get(py_.find(_whitelist_mint, lambda x: py_.get(x, 'name') == 'START_TIME'), 'value', 0)
        _whitelist_end_time = py_.get(py_.find(_whitelist_mint, lambda x: py_.get(x, 'name') == 'END_TIME'), 'value', 0)

        return {
            'whitelist_mint': {
                'start_time': _whitelist_start_time,
                'end_time': _whitelist_end_time
            }
        }

    