from dataclasses import asdict, astuple, dataclass
from pprint import pprint

from stdl import fs


class Dathas:

    def __init__(self) -> None:
        ...

    @property
    def dict(self) -> dict:
        return asdict(self)

    @property
    def tuple(self) -> tuple:
        return astuple(self)

    def print(self):
        pprint(self.dict)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    @classmethod
    def from_json(cls, path: str):
        return cls.from_dict(fs.json_load(path))

    @classmethod
    def from_yaml(cls, path: str):
        return cls.from_dict(fs.yaml_load(path))
