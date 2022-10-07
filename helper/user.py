
from lib.exception import BadRequest
from eth_account.messages import defunct_hash_message
from lib.utils import util_web3, dt_utcnow
from email import message
from operator import truediv
from models import UserModel
import tasks


class UserHelper:
    
    @staticmethod
    def get_sign_message(address):
        if not address:
            raise BadRequest('address can not null')
        _address =  address.lower()
        _nonce = dt_utcnow().timestamp()
        _message = f'I\'m signing to KatanaInu using nonce {_nonce} at address {_address}'
        return {"message":_message,
                "address": _address}
    
    @staticmethod
    def verify_signature(address,message,signature):
        if not address:
            raise BadRequest('address can not null')
        if not message:
            raise BadRequest('message can not null')
        if not signature:
            raise BadRequest('signature can not null')
        _address = address.lower()
        _msg_hash = defunct_hash_message(text=message)
        _signer = util_web3.eth.account.recoverHash(
            _msg_hash,
            signature=signature
        )
        if _address == _signer.lower() :
            _user = UserModel.find_one(
                filter={
                    'address': address.lower()
                }
            )
            if not _user:
                tasks.task_generate_referral_code(_address)
                UserModel.insert_one({
                    'address': _address,
                    'created_by': 'thanh'
                })
                
            return {"message":"Valid!",
                    "address": _address}
        return {"message":"Invalid!"}
        