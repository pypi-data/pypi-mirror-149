from typing import List
from .entity import Entity
from .value_obj import ID


class Repository:
    def __init__(self) -> None:
        pass
    def attach(self, aggregate:Entity)->None:
        raise NotImplementedError
    def detach(self, aggregate:Entity)->None:
        raise NotImplementedError
    def find_by_id(self, id:ID)->Entity:
        raise NotImplementedError
    def find_all(self)->List[Entity]:
        raise NotImplementedError
    def remove(self, aggregate:Entity)->None:
        raise NotImplementedError
    def remove_by_id(self, id: ID)->None:
        raise NotImplementedError
    def save(self, aggregate:Entity)->None:
        raise NotImplementedError
    def save_all(self, aggregates: List[Entity], limit=20) -> None:
        raise NotImplementedError
