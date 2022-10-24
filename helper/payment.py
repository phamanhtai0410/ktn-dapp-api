
from distutils.log import error
from lib.exception import BadRequest
from exception import InvalidNonce, InvalidSignature
from eth_account.messages import defunct_hash_message
from lib.utils import util_web3, dt_utcnow
from email import message
from operator import truediv
from models import PaymentModel




class PaymentHelper:
    
    @staticmethod
    def get_payment_method(chain_id):
        _filter = {
        }
        if chain_id:
            _filter = {
                'chain_id': chain_id
            }

        _payment = PaymentModel.find(
            filter=_filter,
        )

        return {
            'assets': _payment
        }