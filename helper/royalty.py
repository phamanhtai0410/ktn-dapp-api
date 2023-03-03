
from distutils.log import error
from lib.exception import BadRequest
from exception import InvalidNonce, InvalidSignature
from eth_account.messages import defunct_hash_message
from lib.utils import util_web3, dt_utcnow
from email import message
from operator import truediv
# from models import RoyaltyModel, RoyaltyWithdrawHistoryModel, AdminUserModel, CollectionBoxModel, CollectionNFTModel, SignatureLogsModel
from pydash import get


from pymongo import MongoClient
from lib.utils import dt_utcnow
from config import Config
from bson.json_util import dumps
import json

db = MongoClient(Config.MONGO_URI, connect=False)['katana-dapp']

RoyaltyWithdrawHistoryModel = db['royalty_withdraw_history']
RoyaltyModel = db['royalty']
AdminUserModel = db['admin_users']

CollectionNFTModel = db['collection']
CollectionBoxModel = db['boxes']
SignatureLogsModel = db['signature_logs']


class RoyaltyHelper:
    
    @staticmethod
    def get_all_collections_by_user(address):
        _is_admin = False
        # find admin user with address wallet login
        _user_wallet = AdminUserModel.find_one({'address': address})
        if _user_wallet:
            _is_admin = True
            print('vao')
        # find user normal relation to royalty
        if  _is_admin is False:
            # if not admin, find address in collection 'royalty'
            _user_wallet = RoyaltyModel.find_one({'user_address': address})
        if not _user_wallet:
            raise 'Wallet does not exist'
        print(_user_wallet)
        print("_is_admin ", _is_admin)
       
        
        _history_withdraw = RoyaltyWithdrawHistoryModel.find({
            'address': address
        }).sort("block_time", -1).limit(100)

        if _is_admin:
            _find_collections_nft =  list(CollectionNFTModel.find(
                {'created_by': get(_user_wallet, 'email')}
            ).sort('created_time', -1)) # [TODO] get from colleciton boxes | collection
            _find_collections_box =  list(CollectionBoxModel.find({'created_by': get(_user_wallet, 'email')}).sort('created_time', -1))
        else: # royalty
            
            _find_collections_box =  list(CollectionBoxModel.find({'address': get(_user_wallet, 'collection_address')}).sort('created_time', -1))
            _find_collections_nft =  list(CollectionNFTModel.find({'address': get(_user_wallet, 'collection_address')}).sort('created_time', -1))
        
        _collection_nft = []
        _collections_box = []
        if len(_find_collections_box) > 0:
            for _box in _find_collections_box:
                _res_box = {}
                _res_box['name'] = get(_box, 'name')
                if _is_admin:
                    # print("add box ", get(_box, 'address'))
                    _sum_primary_sale = SignatureLogsModel.aggregate([
                        {
                            "$match": {
                                "collection": get(_box, 'address')
                            }
                        },
                        {
                            "$unwind": "$items"
                        },
                        {
                            "$group": {
                                "_id": 0,
                                "total_value": {"$sum": "$items.price_after_discount"}
                            }
                        }
                    ])
                    # print("stages ", list(_sum_primayry_sale))
                    _sum_price = list(_sum_primary_sale)
                    
                    # _sum_primayry_sale[]
                    _res_box['total_income'] = 0 #[TODO] total primary sale and roralty
                    _res_box['primary_sale'] = _sum_price[0].get("total_value", 0) # bsc: get from collection signature_logs (update when mint collection)
                    _res_box['royalty'] = 0 #[TODO]
                else:
                    _res_box['total_income'] = 0
                    _res_box['primary_sale'] = 0
                    _res_box['royalty'] = 0 #[TODO]
                _collections_box.append(_res_box)
        
        if len(_find_collections_nft) > 0:            
            for _nft in _find_collections_nft:
                _res_nft = {}
                _res_nft['name'] = get(_nft, 'name')
                print("get(_nft, 'name') ", get(_nft, 'address'))
                if _is_admin:
                    _sum_primary_sale = SignatureLogsModel.aggregate([
                        {
                            "$match": {
                                "collection": get(_nft, 'address')
                            }
                        },
                        {
                            "$unwind": "$items"
                        },
                        {
                            "$group": {
                                "_id": 0,
                                "total_value": {"$sum": "$items.price_after_discount"}
                            }
                        }
                    ])
                    _res_nft['total_income'] = 0
                    _res_nft['primary_sale'] = _sum_primary_sale
                    _res_nft['royalty'] = 0
                else:
                    _res_nft['total_income'] = 0
                    _res_nft['primary_sale'] = 0
                    _res_nft['royalty'] = 0
                _collection_nft.append(_res_nft)
        _res = {
            'histories_withdraw': _history_withdraw,
            'collection_nft': _collection_nft,
            'collections_box': _collections_box,
            'is_admin': _is_admin
        }
        # print(a)
        _res = json.loads(dumps(_res))
        return _res