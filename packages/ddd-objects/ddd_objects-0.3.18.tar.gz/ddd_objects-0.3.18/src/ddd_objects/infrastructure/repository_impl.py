from typing import List, Dict, Optional, Union
from random import random
from ..domain.repository import Repository
from ..domain.entity import Entity
from ..domain.value_obj import Result, ReturnCode, ValueObject, ID, Page
from ..domain.exception import (
    AlreadyExistsError,
    IDNotExistError,
    NULLError,
    NotExistsError,
    OtherError,
    ParameterError,
    UpdateError,
    OverLimitError,
    KeyExistError,
    OperationError,
    ValueError,
    FormatError,
    WrongReturnCodeError
)
from .ao import exception_class_dec
from .do import BaseDO
from ..lib import Logger

logger = Logger()
logger.set_labels(file_name=__file__)


class RepositoryImpl(Repository):
    def __init__(self, clean_prob=0.1, log_func=None) -> None:
        self.cache = {}
        self.clean_prob = clean_prob
        if log_func is None:
            log_func = logger.info
        self.log_func = log_func

    def attach(self, key: str, obj: BaseDO) -> None:
        if not obj:
            return
        if isinstance(obj, dict):
            return
        if not isinstance(obj, list) \
            and not hasattr(obj, '_expired_time') \
            and not hasattr(obj, 'expired_time'):
            return
        if isinstance(obj, list) \
            and any(not hasattr(m, '_expired_time') for m in obj) \
            and any(not hasattr(m, 'expired_time') for m in obj):
            return
        self.cache[key] = obj

    def clean_cache(self):
        if self.clean_prob<random():
            for key in list(self.cache.keys()):
                x = self.cache[key]
                if (any(m.is_expired for m in x) if isinstance(x, list) else x.is_expired):
                    del self.cache[key]

    def find_from_cache(self, key: str):
        return self.cache.get(key, None)

    def detach(self, aggregate: Entity) -> None:
        raise NotImplementedError

    def find_by_helper(
        self, 
        find_method, 
        key, 
        force_update=False,
        *args,
        **kwargs
    )-> Union[List[Entity], Entity]:
        self.clean_cache()
        x = self.find_from_cache(key)
        if x is None or x.is_expired or force_update:
            x = find_method(*args, **kwargs)
            self.attach(key, x)
        return x

    def find_entity_helper(
        self,
        find_method,
        key,
        converter,
        force_update=False,
        verbose = False,
        *args,
        **kwargs
    )-> Entity:
        self.clean_cache()
        x = self.find_from_cache(key)
        if verbose:
            self.log_func(f'find_entity_helper: cache value is {x}')
        if x is None or (any(m.is_expired for m in x) if isinstance(x, list) else x.is_expired) \
            or force_update:
            x = find_method(*args, **kwargs)
            if converter is not None:
                if isinstance(x, list):
                    x = [converter.to_entity(m) for m in x]
                else:
                    x = converter.to_entity(x)
            if verbose:
                self.log_func(f'find_entity_helper: new value is {x}')
            self.attach(key, x)
        return x

    def find_all_helper(self) -> List[Entity]:
        raise NotImplementedError
    def save_helper(self)->None:
        raise NotImplementedError
    def save_all_helper(self)->None:
        raise NotImplementedError


class SqlalchemyRepositoryImpl(RepositoryImpl):
    def __init__(
        self,
        session_cls,
        do_cls = None
    ) -> None:
        self.session = session_cls()
        self.cache = {}
        self.do_cls = do_cls

    def attach(self, aggregate: Entity) -> None:
        if aggregate.id is None:
            return
        else:
            self.cache[aggregate.id.get_value()] = self.get_json(aggregate)
    
    def detach(self, aggregate: Entity) -> None:
        id = aggregate.id 
        if  id is None or id.get_value() not in self.cache:
            return
        else:
            del self.cache[id.get_value()]

    def get_json(self, aggregate:Entity) -> Dict:
        d = vars(aggregate)
        return {
            key: d[key].get_value() 
                if hasattr(d[key], 'get_value') else d[key] for key in d 
                if d[key].is_changeable and d[key].get_value() is not None
        }

    @exception_class_dec()
    def find_by_id_helper(self, id: ID, do_cls=None)->Optional[Entity]:
        if do_cls is None:
            do_cls = self.do_cls
        result = self.session.query(do_cls).filter(do_cls.id==id.get_value()).all()
        self.session.commit()
        if result:
            return result
        else:
            raise NotExistsError(f'ID({id.get_value()}) not exists')

    @exception_class_dec()
    def find_by_helper(
        self, 
        by_name: str, 
        by: ValueObject, 
        do_cls = None, 
        page: Optional[Page] = None,
        # return_format=list
    )->Optional[List[Entity]]:
        if do_cls is None:
            do_cls = self.do_cls
        if page is None:
            result = self.session.query(do_cls) \
                .filter(getattr(do_cls, by_name)==by.get_value()) \
                .all()
        else:
            result = self.session.query(do_cls) \
                .filter(getattr(do_cls, by_name)==by.get_value()) \
                .limit(page.page_size) \
                .offset(page.get_value()*page.page_size) \
                .all()
        self.session.commit()
        if result:
            return result
        else:
            raise NotExistsError(f'The Object not exists')

    @exception_class_dec()
    def find_all_helper(self, do_cls=None) -> List[BaseDO]:
        if do_cls is None:
            do_cls = self.do_cls
        result = self.session.query(do_cls).all()
        self.session.commit()
        return result

    @exception_class_dec()
    def save_helper(self, x: Entity, do_cls=None, key_mapper={}, ignore_keys=['id']):
        """
        key_mapper: key mapper between Entity and DO, used to convert attributes name
                    format like {entity.key: dto.key}
        """
        if do_cls is None:
            do_cls = self.do_cls
        self.check_unique_keys(x, do_cls, key_mapper, ignore_keys)
        if x.id.get_value() is None:
            x_do = self.converter.to_do(x)
            self.session.add(x_do)
        else:
            if self.find_by_id_helper(x.id, do_cls) is None:
                raise IDNotExistError(f"ID({x.id.get_value()}) doesn't exist")
            d = vars(x)
            key_mapper = {
                key: key_mapper[key] if key in key_mapper else key  for key in d 
                if d[key].get_value is not None 
            }
            x_do = self.converter.to_do(x)
            content = self.get_json(x)
            content = {
                key_mapper[key]: getattr(x_do, key_mapper[key]) for key in content
            }
            if not content:
                raise UpdateError("There's not information can be updated")
            self.session.query(do_cls) \
                .filter(do_cls.id==x.id.get_value()) \
                .update(content, synchronize_session=False)
        self.session.flush()
        self.session.commit()

    @exception_class_dec()
    def save_all_helper(self, aggregates: List[Entity], id_cls, limit=20) -> None:
        # only support insert option
        if len(aggregates)>limit:
            raise OverLimitError(f'The lenght of aritlces if over the limit({limit})')
        for i in range(len(aggregates)):
            aggregates[i].id = id_cls()
        articles_do = [self.converter.to_do(a) for a in aggregates]
        self.session.add_all(articles_do)
        self.session.commit()

    def check_unique_keys(self, x: Entity, do_cls=None, key_mapper={}, ignore_keys=['id']):
        if do_cls is None:
            do_cls = self.do_cls
        d = vars(x)
        unique_keys = [
            key for key in d 
                if d[key] is not None 
                and d[key].get_value() is not None
                and d[key].is_unique and key not in ignore_keys
        ]
        key_mapper = {
            key: key_mapper[key] if key in key_mapper else key  for key in unique_keys
        }
        for key in unique_keys:
            result = self.session.query(do_cls) \
                .add_columns(do_cls.id) \
                .filter(getattr(do_cls, key_mapper[key])==d[key].get_value()) \
                .all()
            self.session.commit()
            if result:
                raise KeyExistError(f'The {key} already exists')
        return True 

class ErrorFactory:
    @staticmethod
    def make(error_code: int):
        if error_code==ReturnCode.SUCCEED_CODE:
            raise WrongReturnCodeError('Wrong error code, 0 is given')
        elif error_code==ReturnCode.NOT_EXIST_CODE:
            return NotExistsError
        elif error_code==ReturnCode.ALREADY_EXIST_CODE:
            return AlreadyExistsError
        elif error_code==ReturnCode.FORMAT_CODE:
            return FormatError
        elif error_code==ReturnCode.VALUE_CODE:
            return ValueError
        elif error_code==ReturnCode.NULL_CODE:
            return NULLError
        elif error_code==ReturnCode.PARAMETER_CODE:
            return ParameterError
        elif error_code==ReturnCode.OPERATION_CODE:
            return OperationError
        elif error_code==ReturnCode.OTHER_CODE:
            return OtherError
        else:
            raise WrongReturnCodeError('Wrong return code')

error_factory = ErrorFactory()

def return_list(log_func=None, return_raw=False):
    def _return_list(func):
        def _f(self, *args, **kwargs):
            result:Result = func(self, *args, **kwargs)
            if result.succeed and result.get_value() is not None and not return_raw:
                return [self.converter.to_entity(r) for r in result.get_value()]
            elif result.succeed and result.get_value() is not None and return_raw:
                return result.get_value()
            elif result.succeed and result.get_value() is None:
                return None
            elif result.return_code.get_value() == ReturnCode.OTHER_CODE:
                if log_func:
                    log_func(result)
                raise OperationError('Operation failed')
            else:
                error_cls = error_factory.make(result.return_code)
                raise error_cls(result.error_info)
        return _f
    return _return_list

def return_single(log_func=None, return_raw=False):
    def _return_single(func):
        def _f(self, *args, **kwargs):
            result:Result = func(self, *args, **kwargs)
            if result.succeed and result.get_value() is not None and not return_raw:
                return [self.converter.to_entity(r) for r in result.get_value()][0]
            elif result.succeed and result.get_value() is not None and return_raw:
                if isinstance(result.get_value(), list):
                    return result.get_value()[0]
                else:
                    return result.get_value()
            elif result.succeed and result.get_value() is None:
                return None
            elif result.return_code.get_value() == ReturnCode.OTHER_CODE:
                if log_func:
                    log_func(result)
                raise OperationError('Operation failed')
            else:
                error_cls = error_factory.make(result.return_code)
                raise error_cls(result.error_info)
        return _f
    return _return_single


def default_log_fun(result: Result):
    print(result.error_info)
    print(result.error_traceback)