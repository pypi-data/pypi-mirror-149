''' mi_models.py
A module to that makes calles to the Infor ION API simple. This module
contains dataclasses that represents data objects from the Api.

Author: Kim Timothy Engh
Email: kim.timothy.engh@epiroc.com
Licence: GPLv3 '''

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional


class Status(Enum):
    ERROR = -1
    EMPTY = 0
    VALID = 1


@dataclass
class Endpoint:
    name: str
    host: str
    port: int
    usr: str
    pwd: str

    def __post_init__(self):
        if not self.pwd: self.pwd = ''

    def __repr__(s):
        return f'Endpoint(name={s.name}, host={s.host}, port={s.port}, usr={s.usr}, pwd={"*" * len(s.pwd)})'


@dataclass
class MiRecords:
    program: str
    transaction: str
    metadata: List[Dict] = field(repr=False)
    records: List[Dict]
    status: Status = field(init=False)

    def __post_init__(self):
        if len(self.records):
            self.status = Status.VALID
        else:
            self.status = Status.EMPTY


@dataclass
class MiPrograms:
    records: List[str]
    status: Status = field(default=Status.EMPTY, init=False)

    def __post_init__(self):
        if len(self.records):
            self.status = Status.VALID


@dataclass
class MiFieldMetadata:
    name: str
    description: str
    fieldtype: str
    length: int
    mandatory: str


@dataclass
class MiTransactionMetadata:
    program: str
    transaction: str
    description: str
    multi: str
    inputs: List[MiFieldMetadata]
    outputs: List[MiFieldMetadata]
    status: Status = field(default=Status.VALID, init=False)


@dataclass
class MiProgramMetadata:
    program: str
    description: str
    version: str
    transactions: List[Optional[MiTransactionMetadata]]
    status: Status = field(default=Status.EMPTY, init=False)

    def __post_init__(self):
        if len(self.transactions):
            self.status = Status.VALID


@dataclass
class MiError:
    code: str
    description: str
    status: Status = field(default=Status.ERROR, init=False)
