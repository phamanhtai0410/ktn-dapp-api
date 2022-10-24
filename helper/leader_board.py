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

        # get leader board and sort with total user input code descending 20 -  1

        _items = PointModel.page(
            filter=_filter,
            func_sort=sort_func,
            sort=-1,
            page=page,
            page_size=page_size
        )
        _items['items'] = [{
            **_item,
            'point': get(_item, 'total_points', 0),
            'rank': page * page_size - (page_size - idex) + 1
        } for idex, _item in enumerate(_items['items'])]
        # for _detail in _items['items']:
        #     _detail['point'] = _detail['total_points']
        #
        #     _more = LeaderBoardModel.find_one(filter={
        #         'address': get(_detail, 'address'),
        #         'event': event
        #     })
        #     _detail['total_points'] = get(_more, 'total_points', 0)
        #
        #     _detail['rank'] = get(_more, 'rank', -1)

        #
        # _leader_board = LeaderBoardModel.page(
        #     filter=_filter,
        #     func_sort=sort_func,
        #     sort=-1,
        #     page=page,
        #     page_size=page_size
        # )

        return _items
