from .mapping import BaseDictKey
from dataclasses import dataclass
from typing import *

__all__ = ['PropertyValueInput', 'CreateARKInput', 'UpdateARKInput']

ARK_NAAN = '45488'

@dataclass
class PropertyValueInput:
    name: str
    value: str


@dataclass
class CreateARKInput(BaseDictKey):
    who: str
    what: str
    where: str
    when: str
    props: List[PropertyValueInput]

    def validate(self):
        errors = []
        if self.who is None:
            errors.append('Field who is required')
        if self.what is None:
            errors.append('Field what is required')
        if self.where is None:
            errors.append('Field where is required')
        if self.when is None:
            errors.append('Field when is required')
        return errors


@dataclass
class UpdateARKInput(BaseDictKey):
    ark: str
    who: str
    what: str
    where: str
    when: str
    props: List[PropertyValueInput]

    def validate(self):
        prefix = 'ark:' + ARK_NAAN + '/'
        errors = []
        if not self.ark:
            errors.append('ark is required')
        elif not self.ark.startswith(prefix) or not self.ark.replace(prefix, '').isalnum():
            errors.append('Invalid ark format. Must be ark:45488/abcdef')
        if self.who is None:
            errors.append('Field who is required')
        if self.what is None:
            errors.append('Field what is required')
        if self.where is None:
            errors.append('Field where is required')
        if self.when is None:
            errors.append('Field when is required')
        return errors
