from typing import Optional
from .dto import FASTAPI_ENV, DTOBase
if FASTAPI_ENV:
    from .dto import BaseModel
from ..domain.entity import Entity

class Assembler:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def assemble_none(fun):
        def f(self, x):
            if x is None:
                return
            else:
                return fun(self, x)
        return f

    def to_entity(self, dto: DTOBase):
        raise NotImplementedError

    def to_dto(self, entity: Optional[Entity]):
        raise NotImplementedError

if FASTAPI_ENV:
    class FastAPIAssembler(Assembler):
        def to_entity(self, dto: BaseModel):
            raise NotImplementedError

