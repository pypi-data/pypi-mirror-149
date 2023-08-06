from typing import Any
from time import time

from .exception import WrongReturnCodeError, ResultFormatError, return_codes


class ValueObject:
    def __init__(self, value=None):
        self.value = value
        self.is_writable = True
        self.is_changeable = True
        self.is_unique = False
    
    def get_value(self):
        return self.value

    def set_unique(self, is_unique=False):
        self.is_unique = is_unique
        return self

    def set_changeable(self, is_changeable=False):
        self.is_changeable = is_changeable
        return self

    def __eq__(self, other):
        if other is None:
            return False
        if not hasattr(other, 'value'):
            return False
        return self.value == other.value

class ExpiredValueObject(ValueObject):
    def __init__(self, value=None, life_time=None):
        super().__init__(value)
        self.life_time = life_time
        if self.life_time is None:
            self.expired_time = None
        else:
            self.expired_time = time()+self.life_time

    @property
    def is_expired(self):
        if self.expired_time is None:
            return False
        else:
            return self.expired_time>time()

class Page(ValueObject):
    def __init__(self, value=None, page_size=10):
        super().__init__(value)
        if value is None:
            self.value = 0
        self.page_size = page_size


class ID(ValueObject):
    def __init__(self, value=None):
        super().__init__(value)
        self.is_writable = False
        self.is_changeable = False
        self.is_unique = True

class ReturnCode(ValueObject):
    SUCCEED_CODE = return_codes['SUCCEED_CODE']
    NOT_EXIST_CODE = return_codes['NOT_EXIST_CODE']
    ALREADY_EXIST_CODE = return_codes['ALREADY_EXIST_CODE']
    FORMAT_CODE = return_codes['FORMAT_CODE']
    PARAMETER_CODE = return_codes['PARAMETER_CODE']
    NULL_CODE = return_codes['NULL_CODE']
    OPERATION_CODE = return_codes['OPERATION_CODE']
    VALUE_CODE = return_codes['VALUE_CODE']
    OTHER_CODE = return_codes['OTHER_CODE']
    def __init__(self, value=None):
        if value is None:
            self.value = self.SUCCEED_CODE
        else:
            super().__init__(value)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name=='value' and (__value>=len(return_codes) or __value<0):
            raise WrongReturnCodeError(f'Wrong return code: {__value}')
        return super().__setattr__(__name, __value)

class Result(ValueObject):
    def __init__(
        self, 
        value=None, 
        succeed=True, 
        return_code:ReturnCode=ReturnCode(), 
        error_info=None,
        error_traceback=None
    ):
        super().__init__(value)
        self.error_info=error_info
        self.error_traceback = error_traceback
        self.succeed = succeed
        self.return_code = return_code

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == 'error_info' and __value is not None and self.value is not None:
            raise ResultFormatError('If error_info is not none, then value must be none')
        return super().__setattr__(__name, __value)

    def get_value(self):
        return self.value

    def get_return_code(self):
        return self.return_code.get_value()
