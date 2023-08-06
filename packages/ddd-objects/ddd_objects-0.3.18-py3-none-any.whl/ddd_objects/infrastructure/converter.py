from ..domain.entity import Entity
from .do import SQLALCHEMY_ENV, BaseDO
if SQLALCHEMY_ENV:
    from .do import SqlalchemyBase

class Converter:
    def __init__(self) -> None:
        pass
    @staticmethod
    def convert_none(fun):
        def f(self, x):
            if x is None:
                return
            else:
                return fun(self, x)
        return f
    def to_do(self, entity: Entity):
        raise NotImplementedError
    def to_entity(self, do: BaseDO):
        raise NotImplementedError
    def to_value(self, do: BaseDO):
        raise NotImplementedError
        
if SQLALCHEMY_ENV:
    class SqlalchemyConverter(Converter):
        def to_entity(self, do: SqlalchemyBase):
            raise NotImplementedError
        def to_value(self, do: SqlalchemyBase):
            raise NotImplementedError
