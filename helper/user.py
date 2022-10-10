
from lib.exception import BadRequest
from eth_account.messages import defunct_hash_message
from lib.utils import util_web3, dt_utcnow
from email import message
from operator import truediv
from models import UserModel
from tasks import referral
from .wallet import WalletHelper


class UserHelper:
    
    @staticmethod
    def validate_nonce(_nonce):
        _dt = dt_utcnow().timestamp() - _nonce
        if 10000 >= _dt >= 0:
            return True

        return False

    
    @staticmethod
    def get_sign_message(address):
        if not address:
            raise BadRequest('address can not null')
        _address =  address.lower()
        _message,_nonce = WalletHelper.get_sign_msg(_address)
        return {"message":_message,
                "address": _address,
                "nonce":_nonce}
    
    @classmethod
    def verify_signature(cls, address,nonce,signature):
        if not address:
            raise BadRequest('address can not null')
        if not nonce:
            raise BadRequest('nonce can not null')
        if not signature:
            raise BadRequest('signature can not null')
        
        check = cls.validate_nonce(nonce)
        if check ==False: 
            raise BadRequest('nonce is invalid')
        _address = address.lower()
        _message = WalletHelper._get_sign_msg(_address, nonce)
        _signer = WalletHelper.get_address_of(signature,_message)
        if _address == _signer:
            _user = UserModel.find_one(
                filter={
                    'address': _address
                }
            )
            if not _user:
                referral.task_generate_referral_code.delay(address = _address) 
                UserModel.insert_one({
                    'address': _address,
                    'created_by': 'thanh'
                })
               
            return {"result":"Valid!",
                    "address": _address}
        return {"result":"Invalid!"}
        