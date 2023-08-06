from abc import ABC, abstractmethod
from enum import Enum


class ValidationRule(ABC):

    @abstractmethod
    def execute(self):
        ...

    def getUpdatedValue(self, key):
        """
        get update attribute, dto object (user value) has priority

        :param key:
        :return:
        """
        dto_attr = getattr(self, key)

        if isinstance(dto_attr["dto"], Enum):
            if dto_attr["dto"].value is not None:
                return dto_attr["dto"]
        else:
            if dto_attr["dto"] is not None:
                return dto_attr["dto"]

        if isinstance(dto_attr["db"], Enum):
            if dto_attr["db"].value is not None:
                return dto_attr["db"]
        else:
            if dto_attr["db"] is not None:
                return dto_attr["db"]

        return dto_attr["dto"]
