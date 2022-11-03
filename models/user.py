# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from models import DaoModel


class UserDao(DaoModel):
    def __init__(self, *args, **kwargs):
        super(UserDao, self).__init__(*args, **kwargs)
