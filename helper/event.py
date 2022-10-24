# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from models import EventModel


class EventHelper:

    @staticmethod
    def get_statistical(event_name):
        _result = EventModel.find_one({
            'name': event_name
        })
        return _result or {}