# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""


class ReRateEx(Exception):
    def __init__(self, msg='You cannot re-rate.', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_RE_RATE'

    pass
