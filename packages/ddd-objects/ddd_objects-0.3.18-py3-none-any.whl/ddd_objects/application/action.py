import inspect
from typing import List

from ..domain.exception import OperationError
from ..domain.repository import Repository
from ..domain.value_obj import Page
from ..domain.entity import Entity
try: 
    from fastapi import HTTPException
    FASTAPI_ENV = True
except:
    FASTAPI_ENV = False

if FASTAPI_ENV:
    def fastapi_exception_helper(func):
        def _f(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                raise HTTPException(status_code=400, detail={
                    "error_info": str(e),
                    "return_code": e.return_code
                })
            return result
        return _f
def exception_helper(func):
    def _f(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            raise Exception(str(e))
        return result
    return _f


def action_get_by_helper(
    repo: Repository, 
    assembler_cls, 
    by, 
    find_method='find_by_id', 
    page: Page=None
):
    find_func = getattr(repo, find_method)
    if 'page' in inspect.getfullargspec(find_func)[0]:
        xs = find_func(by, page=page)
    else:
        xs = find_func(by)
    assembler = assembler_cls()
    if xs is None:
        return None
    elif isinstance(xs, list):
        return [assembler.to_dto(x) for x in xs]
    else:
        return assembler.to_dto(xs)

def action_get_all_helper(repo: Repository, assembler_cls):
    xs:List[Entity] = repo.find_all()
    if xs is None:
        raise OperationError('Operation failed')
    assembler = assembler_cls()
    return [assembler.to_dto(x) for x in xs]

def action_save_helper(repo: Repository, dto, assembler_cls):
    assembler = assembler_cls()
    x: Entity = assembler.to_entity(dto)
    result =  repo.save(x)
    if result is None:
        raise OperationError('Operation failed')

def action_save_all_helper(repo: Repository, dtos, assembler_cls):
    assembler = assembler_cls()
    xs = [assembler.to_entity(dto) for dto in dtos]
    result = repo.save_all(xs)
    if result is None:
        raise OperationError('Operation failed')