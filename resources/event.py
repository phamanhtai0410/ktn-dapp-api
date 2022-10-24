# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get

from connect import security
from helper.event import EventHelper
from schemas.event import EventParam, EventSchema


class EventResource(Resource):

    @security.http(
        params=EventParam(),
        response=EventSchema()
    )
    def get(self, params):
        return EventHelper.get_statistical(get(params,'name'))
