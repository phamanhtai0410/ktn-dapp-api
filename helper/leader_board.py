from constants import Constants
from lib.exception import BadRequest
from models import LeaderBoardModel
import pydash as py_

class LeaderBoardHelper:

    @staticmethod
    def get_top_referral_leader_board(event, page, page_size, search):

        _filter = {
            'event': event
        }
        if search:
            _filter = {
                **_filter,
                'address': search
            }

        sort_func = lambda x: py_.get(x, 'point', 0)

        # get leader board and sort with total user input code descending
        _leader_board = LeaderBoardModel.page(
            filter=_filter,
            func_sort=sort_func,
            sort= -1,
            page=page,
            page_size=page_size
        )

        return _leader_board
