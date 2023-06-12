# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from models import DaoModel


class RoyaltyDao(DaoModel):
    def __init__(self, *args, **kwargs):
        super(RoyaltyDao, self).__init__(*args, **kwargs)
        
class RoyaltyWithdrawHistoryDao(DaoModel):
    def __init__(self, *args, **kwargs):
        super(RoyaltyWithdrawHistoryDao, self).__init__(*args, **kwargs)
        
class AdminUserDao(DaoModel):
    def __init__(self, *args, **kwargs):
        super(AdminUserDao, self).__init__(*args, **kwargs) 

class CollectionBoxDao(DaoModel):
    def __init__(self, *args, **kwargs):
        super(CollectionBoxDao, self).__init__(*args, **kwargs) 
        
class CollectionNFTDao(DaoModel):
    def __init__(self, *args, **kwargs):
        super(CollectionNFTDao, self).__init__(*args, **kwargs)

class NFTDao(DaoModel):
    def __init__(self, *args, **kwargs):
        super(NFTDao, self).__init__(*args, **kwargs)
          

class SignatureLogsDao(DaoModel):
    def __init__(self, *args, **kwargs):
        super(SignatureLogsDao, self).__init__(*args, **kwargs)
        
