from time import time
from typing import Optional


class Entity:
    def get_json(self):
        raise NotImplementedError

class ExpiredEntity(Entity):
    def __init__(self, _life_time:Optional[int]=None) -> None:
        self._life_time = _life_time
        if self._life_time is None:
            self._expired_time = None
        else:
            self._expired_time = time()+self._life_time.get_value()

    @property
    def is_expired(self):
        if self._expired_time is None:
            return False
        else:
            return self._expired_time<time()