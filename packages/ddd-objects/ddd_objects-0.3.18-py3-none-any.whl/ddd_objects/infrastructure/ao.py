import traceback, json, requests
from ..domain.value_obj import ReturnCode, Result
from .do import BaseDO
class AOResult(Result):
    pass

def exception_dec(max_try=3):
    def _exception_helper(func):
        def _f(*args, **kwargs):
            for _ in range(max_try):
                try:
                    return AOResult(func(*args, **kwargs))
                except Exception as e:
                    if hasattr(e, 'return_code'):
                        return_code = ReturnCode(e.return_code)
                    else:
                        return_code = ReturnCode(ReturnCode.OTHER_CODE)
                    error_info = str(e)
                    error_traceback = traceback.format_exc()
            else:
                return AOResult(
                    succeed=False, 
                    return_code=return_code, 
                    error_info=error_info,
                    error_traceback=error_traceback
                )
        return _f
    return _exception_helper

def exception_class_dec(max_try=3):
    def _exception_class_helper(func):
        def _f(self, *args, **kwargs):
            for _ in range(max_try):
                try:
                    return AOResult(func(self, *args, **kwargs))
                except Exception as e:
                    error_info = str(e)
                    error_traceback = traceback.format_exc()
                    if hasattr(e, 'return_code'):
                        return_code = ReturnCode(e.return_code)
                        return AOResult(
                            succeed=False, 
                            return_code=return_code, 
                            error_info=error_info,
                            error_traceback=error_traceback
                        )
                    else:
                        return_code = ReturnCode(ReturnCode.OTHER_CODE)
            else:
                return AOResult(
                    succeed=False, 
                    return_code=return_code, 
                    error_info=error_info,
                    error_traceback=error_traceback
                )
        return _f
    return _exception_class_helper

def service_exception_helper(url:str, do: BaseDO, max_try=3):
    for _ in range(max_try):
        try:
            data = do.to_json()
            data = json.dumps(data)
            response=requests.post(url, data=data, timeout=60)
            return AOResult(json.loads(response.text))
        except Exception as e:
            if hasattr(e, 'return_code'):
                return_code = ReturnCode(e.return_code)
            else:
                return_code = ReturnCode(ReturnCode.OTHER_CODE)
            error_info = str(e)
            error_traceback = traceback.format_exc()
    else:
        return AOResult(
            succeed=False, 
            return_code=return_code, 
            error_info=error_info,
            error_traceback=error_traceback
        )
