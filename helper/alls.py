# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import re

from models import CollectionNFTModel, CollectionBoxModel, NFTModel, NftWhitelistModel, EmailSubscribeModel
from pydash import get
import pydash as py_

from lib import dt_utcnow


REGEX_EMAIL = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

class AllsItemHelper:
    @staticmethod
    def get_user_whitelist_amount(collection, user_address):
        _nft_whitelist = NftWhitelistModel.find_one({
            'collection': collection,
            'address': user_address
        }, cache=True)
        return py_.get(_nft_whitelist, 'amount', 0)

    @staticmethod
    def get_user_minted_amount(collection_address, user_address):
        _count = NFTModel.col.count_documents({
            'contract': collection_address,
            'address': user_address
        })

        return _count

    @staticmethod
    def get_whitelist_time(collection):
        _whitelist_time = get(collection, 'whitelist_time', [])
        _defaul_whitelist_time = {
                'start_time': None,
                'end_time': None
            }
        if not _whitelist_time:
            return _defaul_whitelist_time
        _now = dt_utcnow()
        py_.sort(_whitelist_time, key=lambda x: py_.get(x, 'end_time'))

        # NOTE: find nearest whitelist time
        _whitelist = py_.find(_whitelist_time, lambda x: py_.get(x, 'start_time') <= _now.timestamp())

        # NOTE: if not whitelist time start yet -> return nearest end_time whitelist
        if not _whitelist:
            return py_.get(_whitelist_time, '0')
        
        return _whitelist

    @staticmethod
    def get_collection_data(collection, nft_id=None, user_address=None):
        _items = []
        if not collection:
            return _items

        if get(collection, 'address') and get(collection, 'types_list'):
            _total_user_minted = 0
            _user_whitelist_amount = 0
            if user_address:
                _total_user_minted = AllsItemHelper.get_user_minted_amount(
                    collection_address=get(collection, 'address'),
                    user_address=user_address)
                _user_whitelist_amount = AllsItemHelper.get_user_whitelist_amount(
                    collection=get(collection, 'address'),
                    user_address=user_address)

            _types_list = get(collection, 'types_list')
            _is_box = get(collection, 'is_box')
            _whitelist = AllsItemHelper.get_whitelist_time(collection=collection)
            _nft_info = {
                'nft_id': 0, # NOTE: if collection mint like box only need index 0
                'name': get(collection, 'name'),
                'address': get(collection, 'address'),
                'chain': get(collection, 'chain'),
                'chain_id': get(collection, 'chain_id'),
                'pay_token_address': get(collection, 'pay_token_address'),
                'dapp_creator_address': get(collection, 'dapp_creator_address'),
                'whitelist': _whitelist,
                'total_user_minted': _total_user_minted,
                'user_whitelist_amount': _user_whitelist_amount
            }
            if _is_box:
                _total_minted = NFTModel.col.count_documents({
                    'contract': get(collection, 'address')
                })
                _items.append({
                    **_nft_info,
                    'nft_id': 0, # NOTE: if collection mint like box only need index 0
                    'price': get(_types_list, '0.price', 0), # NOTE: if box will get same price from first nft
                    'image': get(collection, 'box_image_url', ''),
                    'rarity': get(_types_list, '0.AssetRarity'),
                    'total_supply': get(collection, 'total_supply', 0),
                    'total_minted': _total_minted,
                })
            elif nft_id is not None:
                _nft = get(_types_list, f'{nft_id}', None)
                _count_filter = {
                    'contract': get(collection, 'address')
                }
                if not _is_box:
                    _count_filter = {
                        **_count_filter,
                        'nft_index': nft_id
                    }
                _total_minted = NFTModel.col.count_documents(_count_filter)

                _items = [{
                    **_nft_info,
                    'nft_id': nft_id, # NOTE: this nft_id is index of nft in collection for mint
                    'price': get(_nft, 'price', 0),
                    'image': get(_nft, 'ImageUrl', '') if not _is_box else get(collection, 'box_image_url'),
                    'animation_model_url': get(_nft, 'AnimationModelUrl', '') if not _is_box else get(collection, 'box_image_url'),
                    'rarity': get(_nft, 'AssetRarity'),
                    'total_supply': int(get(collection, 'total_supply', 0) if not _is_box else get(collection, 'total_supply') * get(_nft, 'rate') / 100),
                    'total_minted': _total_minted,
                }] if _nft else []

            else:
                for (_idx, _type) in enumerate(_types_list):
                    _total_minted = NFTModel.col.count_documents({
                        'contract': get(collection, 'address'),
                        'nft_index': _idx  #NOTE: if not type box -> supply will by each nft rate
                    })
                    _items.append({
                        **_nft_info,
                        'nft_id': _idx, # NOTE: this nft_id is index of nft in collection for mint
                        'price': get(_type, 'price', 0),
                        'image': get(_type, 'ImageUrl', ''),
                        'animation_model_url': get(_type, 'AnimationModelUrl', ''),
                        'rarity': get(_type, 'AssetRarity'),
                        'total_supply': int(get(collection, 'total_supply', 0) * get(_type, 'rate') / 100),
                        'total_minted': _total_minted,
                    })

        return _items

    @staticmethod
    def paging(data, page, page_size):

        _offset = page_size * (page - 1)
        _limit = (int(page * page_size))
        _offset = int(_limit - page_size)

        _data = data[_offset:_limit]
        _num_of_page = (len(data) / page_size)
        if (len(data) % page_size) > 0:
            _num_of_page = _num_of_page + 1

        _result = {
            'items': _data,
            'num_of_page': _num_of_page,
            'page_size': page_size,
            'page': page
        }

        return _result

    @staticmethod
    def get_by_filter(params={}):
        print(params)
        _now = dt_utcnow().timestamp()
        _filter = {
            'deployed': True
        }
        if get(params, 'chain'):
            _filter['chain'] = get(params, 'chain')
        if get(params, 'category'):
            _filter['category'] = get(params, 'category')
        if get(params, 'state') and get(params, 'state') == 'current_live':
            _filter['whitelist_time.start_time'] = {
                "$lt": _now
            }
        _collections = list(CollectionNFTModel.find(filter=_filter))
        _items = []
        if len(_collections):
            for _collection in _collections:
                _collection_data = AllsItemHelper.get_collection_data(collection=_collection)
                if get(params, 'state') and get(params, 'state') == 'last_sold_out':
                    for _i in _collection_data:
                        if get(_i, 'total_minted') == get(_i, 'total_supply'):
                            _items.append(_i)
                else:
                    _items = [
                        *_items,
                        *_collection_data
                    ]

        _page = get(params, 'page')
        _page_size = get(params, 'page_size')
        
        _result = AllsItemHelper.paging(
            data=_items,
            page=_page,
            page_size=_page_size
        )

        return _result or {}
    
    @staticmethod
    def get_one_by_filter(params={}):
        _filter = {
            'deployed': True
        }
        _address = get(params, 'address').lower()
        _user_address = get(params, 'user_address', '').lower()
        _filter["address"] = _address
        if get(params, 'chain'):
            _filter['chain'] = get(params, 'chain')
        if get(params, 'category'):
            _filter['category'] = get(params, 'category')
        _collections = CollectionNFTModel.find_one(filter=_filter)
        if not _collections:
            return {
                'items': []
            }

        _nft_id = get(params, 'nft_id', None)
        _items = AllsItemHelper.get_collection_data(
            collection=_collections,
            nft_id=_nft_id,
            user_address=_user_address
        )

        _result = {
            'items': _items,
        
        }
        return _result or {}
    
    @staticmethod
    def get_upcoming(params={}):

        return {}
    
    
    @staticmethod
    def check_email_subscirbe(_email):
        if re.fullmatch(REGEX_EMAIL, _email):
            return True
        return False
    
    @staticmethod
    def update_email_subscirbe(_email):
        find_one = EmailSubscribeModel.find_one({"email": _email})
        if find_one:
            return
        EmailSubscribeModel.insert_one({
            "email": _email,
            "created_by": "user",
            "created_time": dt_utcnow(),
            "updated_time": dt_utcnow()
        })