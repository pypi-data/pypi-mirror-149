return_codes = {
    'SUCCEED_CODE': 0,
    'NOT_EXIST_CODE': 1,
    'ALREADY_EXIST_CODE': 2,
    'FORMAT_CODE':  3,
    'PARAMETER_CODE': 4,
    'NULL_CODE': 5,
    'OPERATION_CODE': 6,
    'VALUE_CODE': 7,
    'OTHER_CODE': 8,
}
class BaseError(Exception):
    def __init__(self, error_info:str, return_code: int, *args: object) -> None:
        '''
        return_code 与 value_obj中的ReturnCode相对应
        '''
        super().__init__(error_info, *args)
        self.return_code = return_code

class NotExistsError(BaseError):
    def __init__(self, error_info: str, *args: object) -> None:
        return_code = return_codes['NOT_EXIST_CODE']
        super().__init__(error_info, return_code, *args)

class AlreadyExistsError(BaseError):
    def __init__(self, error_info: str, *args: object) -> None:
        return_code = return_codes['ALREADY_EXIST_CODE']
        super().__init__(error_info, return_code, *args)

class FormatError(BaseError):
    def __init__(self, error_info: str, *args: object) -> None:
        return_code = return_codes['FORMAT_CODE']
        super().__init__(error_info, return_code, *args)

class ParameterError(BaseError):
    def __init__(self, error_info: str, *args: object) -> None:
        return_code = return_codes['PARAMETER_CODE']
        super().__init__(error_info, return_code, *args)

class NULLError(BaseError):
    def __init__(self, error_info: str, *args: object) -> None:
        return_code = return_codes['NULL_CODE']
        super().__init__(error_info, return_code, *args)

class OperationError(BaseError):
    def __init__(self, error_info: str, *args: object) -> None:
        return_code = return_codes['OPERATION_CODE']
        super().__init__(error_info, return_code, *args)


class ValueError(BaseError):
    def __init__(self, error_info: str, *args: object) -> None:
        return_code = return_codes['VALUE_CODE']
        super().__init__(error_info, return_code, *args)

class OtherError(BaseError):
    def __init__(self, error_info: str, *args: object) -> None:
        return_code = return_codes['OTHER_CODE']
        super().__init__(error_info, return_code, *args)

class IDNotExistError(NotExistsError):
    pass

class UpdateError(OperationError):
    pass

class OverLimitError(ValueError):
    pass

class KeyExistError(AlreadyExistsError):
    pass

class WrongReturnCodeError(Exception):
    pass

class ResultFormatError(FormatError):
    pass

