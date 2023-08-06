from dataclasses import dataclass
from typing import *
import typing

__all__ = ['ARK', 'get_fragments', 'PropertyValue']


@dataclass(order=True, frozen=True)
class BaseDictKey:
    """
    Inheriting from this class is identical to making each field Optional and None by default
    """
    def __init_subclass__(cls, *args, **kwargs):
        for field, value in cls.__annotations__.items():
            cls.__annotations__[field] = typing.Union[value, None]
            if not hasattr(cls, field):
                setattr(cls, field, None)
        super().__init_subclass__(*args, **kwargs)


@dataclass
class PropertyValue:
    name: str
    value: str

    @staticmethod
    def gql_fragment():
        return """
            fragment propsFields on PropertyValue {
              name
              value
            }
            """


@dataclass
class ARK(BaseDictKey):
    ark: str
    who: str
    what: str
    where: str
    when: str
    props: List[PropertyValue]

    @staticmethod
    def gql_fragment():
        return """
            fragment arkFields on ARK {
              ark
              who
              what
              where
              when
              props {
                ...propsFields
              }
            }
        """


def get_fragments():
    return f"""
            {PropertyValue.gql_fragment()}
            {ARK.gql_fragment()}
        """
