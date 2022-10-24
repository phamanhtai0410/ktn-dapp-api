from pydash import get

from constants import Constants
from lib.exception import BadRequest
from models import LeaderBoardModel, PointModel
import pydash as py_


class LeaderBoardHelper:

    @staticmethod
    def get_leader_board(event, page, page_size, search):

        _filter = {
            'event': event
        }
        if search:
            _filter = {
                **_filter,
                'address': search.lower()
            }

        sort_func = lambda x: py_.get(x, 'total_points', 0)

        # get leader board and sort with total user input code descending

        _items = PointModel.page(
            filter=_filter,
            func_sort=sort_func,
            sort=-1,
            page=page,
            page_size=page_size
        )
        for _detail in _items['items']:
            _detail['point'] = _detail['total_points']

            _detail['total_points'] = get(LeaderBoardModel.find_one(filter={
                'address': get(_detail, 'address'),
                'event': event
            }), 'point', 0)
        #
        # _leader_board = LeaderBoardModel.page(
        #     filter=_filter,
        #     func_sort=sort_func,
        #     sort=-1,
        #     page=page,
        #     page_size=page_size
        # )

        return _items
