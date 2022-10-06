from constants import Constants
from lib.exception import BadRequest
from models import LeaderBoardModel
import pydash as py_

class LeaderBoardHelper:

    @staticmethod
    def get_top_referral_leader_board(page, page_size, search):

        _filter = {
            'event': Constants.TOP_REFERRAL_EVENT_NAME
        }
        if search:
            _filter = {
                **_filter,
                'public_address': search
            }

        # get leader board and sort with total user input code descending
        _leader_board = LeaderBoardModel.page(
            filter={},
            func_sort=lambda x: py_.get(x, 'total_user_linked', 0),
            sort= -1,
            page=page,
            page_size=page_size
        )

        return _leader_board