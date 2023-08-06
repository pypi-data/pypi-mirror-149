''' mi_api.py
The mi_api file, part of the getting-and-setting package contains functions
combines functions from parser.py and request.py to provide abstract tools to
work with the MI Api.

Author: Kim Timothy Engh
Email: kim.timothy.engh@epiroc.com
Licence: GPLv3. See ../LICENCE '''

from typing import Union
from typing import Optional

from . mi_models import MiRecords
from . mi_models import MiPrograms
from . mi_models import MiProgramMetadata
from . mi_models import MiTransactionMetadata
from . mi_models import MiError

from . mi_parser import mi_parse_execute
from . mi_parser import mi_parse_metadata
from . mi_parser import mi_parse_programs

from . mi_request import mi_request_metadata
from . mi_request import mi_request_execute
from . mi_request import mi_request_programs


class MiApi:
    def __init__(self, host: str, port: int, usr: str, pwd: str):
        self.host = host
        self.port = port
        self.usr = usr
        self.pwd = pwd

    def execute(self, program: str, transaction: str, **kwargs) -> Union[MiRecords, MiError]:
        return mi_parse_execute(
            mi_request_execute(
                self.host,
                self.port,
                self.usr,
                self.pwd,
                program,
                transaction,
                **kwargs
            ).content
        )

    def program_list(self) -> Union[MiPrograms, MiError]:
        return mi_parse_programs(
            mi_request_programs(
                self.host,
                self.port,
                self.usr,
                self.pwd
            ).content
        )

    def program_meta(self, program: str) -> Union[MiProgramMetadata, MiError]:
        return mi_parse_metadata(
            mi_request_metadata(
                self.host,
                self.port,
                self.usr,
                self.pwd,
                program
            ).content
        )

    def transaction_meta(self, program: Optional[str], transaction: Optional[str]) -> Union[MiTransactionMetadata, MiError, None]:
        program_meta = self.program_meta(program)

        if isinstance(program_meta, MiError):
            return program_meta

        elif program_meta.status:
            for record in program_meta.transactions:
                if record.transaction == transaction:
                    return record
        else:
            return None
