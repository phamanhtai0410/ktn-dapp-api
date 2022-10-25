# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from lib import DaoModel


class PointDao(DaoModel):
    def __init__(self, *args, **kwargs):
        super(PointDao, self).__init__(*args, **kwargs)

    def key_of_event(self, event):
        return f'ktn:points:events:{event}'

    def get_rank(self, event, page, page_size):
        if page <= 0:
            page = 1
        _start = (page - 1) * page_size
        _end = page * page_size
        _rank = self.redis.zrange(self.key_of_event(event), _start, _end,  withscores=True)

