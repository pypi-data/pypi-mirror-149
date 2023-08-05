''' mi_api.py
The mi_api file, part of the getting-and-setting package contains functions
combines functions from parser.py and request.py to provide abstract tools to
work with the MI Api.

Author: Kim Timothy Engh
Email: kim.timothy.engh@epiroc.com
Licence: GPLv3. See ../LICENCE '''

from typing import Union
from . import parser
from . import mi


class MiApi:
    def __init__(self, ip: int, port: str, usr: str, pwd: str):
        self.ip = ip
        self.port = port
        self.usr = usr
        self.pwd = pwd

    def query(self, program: str, transaction: str, **kwargs) -> Union[parser.MiData, parser.MiError]:
        ''' Make an API request. Note the the **kwargs represents the possible
        input fields for the API, ususally the column names. Refer to documenation
        for the specific API. If max_recs is passed the maximum number of return
        rows will be modified. Note that if 0 is given as max_recs, all records
        will be retured.

        Examples of usage:
        >> mi_api = MiApi('server.company', 21000, 'a_username', 'a_password')
        >> query = mi_api.query('MMS005MI', 'SelRoute', max_recs=0, EDES='AAA')

        The function will return a MiData object if no errors are raised by the api,
        else it will return a MiError object with information about the error.
        '''

        api = mi.Api(self.ip, self.port, self.usr, self.pwd)
        result = api.request(program, transaction, **kwargs)

        return result