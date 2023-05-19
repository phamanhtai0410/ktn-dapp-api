from pydash import get

from constants import Constants
from lib.exception import BadRequest
from models import LeaderBoardModel, PointModel, ReferralLogModel
import pydash as py_


class LeaderBoardHelper:

    @staticmethod
    def get_leader_board(event, page, page_size, search):
        _filter = {
            'event': event
        }

        if event == 'top_referral':

            if search:
                _total_ref_people = ReferralLogModel.col.count_documents(
                    {
                        'address_linked': search
                    }
                )
                _rank = LeaderBoardModel.get_rank_of(
                        event=event,
                        address=search.lower()
                    )
                return {
                    "items": [
                        {
                            **_rank,
                            'total_referral_people': _total_ref_people
                        }    
                    ],
                    'num_of_page': 1,
                    'page_size': page_size,
                    'page': page
                }

            def func_filter(item):
                if search:
                    if search.lower() == get(item, 'address'):
                        return True
                    return False

                return True

            sort_func = lambda x: py_.get(x, 'point', 0)

            # get leader board and sort with total user input code descending
            _leader_board = LeaderBoardModel.page(
                filter=_filter,
                func_sort=sort_func,
                sort=-1,
                page=page,
                page_size=page_size,
                cache=True,
                func_filter=func_filter,
                hset_field='address'
            )
            # if search:
            _leader_board['items'] = [{
                **value,
                'rank': page * page_size - (page_size - _index) + 1
            } for _index, value in enumerate(_leader_board['items'])]
            return _leader_board
        # sort_func = lambda x: py_.get(x, 'total_points', 0)

        # get leader board and sort with total user input code descending 20 -  1
        if search:
            search = search.lower()
            _rank = PointModel.get_rank_of(
                event=event,
                address=search
            )
            _point = get(PointModel.find_one({
                'event': event,
                'address': search
            }), 'total_points', 0) if _rank else 0
            return {
                'items': [{
                    'rank': _rank,
                    'point': _point,
                    'address': search
                }],
                'num_of_page': 1,
                'page_size': 1,
                'page': 1
            }
        else:
            _items, num_of_page = PointModel.get_rank(
                event=event,
                page=page,
                page_size=page_size
            )
            return {
                "items": _items,
                'num_of_page': num_of_page,
                'page_size': page_size,
                'page': page
            }
        # _items['items'] = [{
        #     **_item,
        #     'point': get(_item, 'total_points', 0),
        #     'rank': page * page_size - (page_size - idex) + 1
        # } for idex, _item in enumerate(_items['items'])]
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
