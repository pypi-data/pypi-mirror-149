from ddd_objects.application.action import FASTAPI_ENV


try:
    from pydantic import BaseModel
    FASTAPI_ENV = True
except:
    FASTAPI_ENV = False

class DTOBase:
    pass