from enum import Enum


class RegexEnum(Enum):
    NAME = (
        r'^[A-Z][a-z]{,19}$',#r щоб вважало все стрвінгою
        'Only alpha characters are allowed.'
    )

    def __init__(self, pattern: str, msg: str):
        self.pattern = pattern
        self.msg = msg
