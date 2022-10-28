# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from models import DaoModel


class ReferralLogDao(DaoModel):
    def __init__(self, *args, **kwargs):
        super(ReferralLogDao, self).__init__(*args, **kwargs)
