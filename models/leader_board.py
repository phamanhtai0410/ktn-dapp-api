# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from pydash import get

from lib import DaoModel


class LeaderBoardDao(DaoModel):
    def __init__(self, *args, **kwargs):
        super(LeaderBoardDao, self).__init__(*args, **kwargs)

    def get_rank_of(self, event, address):

        _list = self.find(filter={
            'event': event
        }, hset_field='address', cache=True)
        _list.sort(key=lambda x: x.get('point'), reverse=True)
        for _rank, val in enumerate(_list):
            if get(val, 'address') == address:
                return {
                    **val,
                    'rank': _rank + 1
                }

        return {
            'rank': -1,
            'point': 0,
            'address': address
        }
