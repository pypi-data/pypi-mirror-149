#######################################################
# Execution ray
#######################################################
import random
import uuid
from typing import Dict

from tqdm.asyncio import tqdm, tqdm_asyncio


class OpenfabricExecutionRay:
    __bars: Dict[str, tqdm_asyncio] = None
    __id: str = None

    def __init__(self, session_id):
        self.__bars = dict()
        self.__id = session_id

    def session_id(self):
        if self.__id is None:
            self.__id = uuid.uuid4().hex
        return self.__id

    def progress(self, name, total=100) -> tqdm_asyncio:
        if self.__bars.get(name) is None:
            self.__bars[name] = tqdm(total=total)
        return self.__bars[name]

    def all_progress(self):
        return self.__bars
