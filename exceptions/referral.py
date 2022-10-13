from lib.exception import BadRequest

class InvalidReferralCodeEx(Exception):
    def __init__(self, msg='Referral code is invalid.', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_INVALID_REFERRAL_CODE'

    pass

class InvalidUserInputOwnCode(Exception):
    def __init__(self, msg="user can not input user's own code", *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_INVALID_USER_INPUT_OWN_CODE'

    pass

class InvalidUserHasInputCode(Exception):
    def __init__(self, msg="user has been linked with another code", *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_INVALID_USER_HAS_INPUT_CODE'

    pass