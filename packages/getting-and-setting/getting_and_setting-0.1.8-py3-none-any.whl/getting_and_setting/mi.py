''' api.py
A module to that makes calles to the Infor ION API simple. This moduele
handels url creation, authentication and requests. Reconmended way to use
this moduel is by using the class Api.

Author: Kim Timothy Engh
Email: kim.timothy.engh@epiroc.com
Licence: GPLv3 '''


from typing import Optional
import requests
from requests.auth import HTTPBasicAuth


def dict_to_param_str(param_dict: dict) -> str:
    '''
    Convert a dict with key values and return a parameter string to
    be used as parameters in a request url. Note that the argument
    max_recs is treaded as a special case and is added in the string
    before the search parameters.

    >>> dict_to_param_str({'EDES': 'AU1'})
    '?EDES=AU1'

    >>> dict_to_param_str({'WHSL': 'AUA', 'ROUT': 'AA0001'})
    '?WHSL=AUA&ROUT=AA0001'

    >>> dict_to_param_str({'max_recs': 0, 'WHSL': 'AUA', 'ROUT': 'AA0001'})
    ';max_recs=0;?WHSL=AUA&ROUT=AA0001'
    '''

    max_recs = f';max_recs={param_dict.pop("max_recs")};' if param_dict.get("max_recs") != None else ''

    params_str = r'&'.join(
        [
            f'{key}={value}'
            for key, value
            in param_dict.items()
        ]
    )

    return f'{max_recs}?{params_str}'


def create_url(
    ip: str, port: str, program: str,
    transaction: str, params: Optional[str] = ''
    ) -> str:
    ''' Takes an ip, port, program, transaction and the params as a str and returns
    a url to use for the API request.

    >>> create_url('server.company', '21100', 'DRS005MI', 'SelRoute', '?WHLO=AAA&ROUT=AA0001')
    'http://server.company:21100/m3api-rest/execute/DRS005MI/SelRoute?WHLO=AAA&ROUT=AA0001'

    >>> create_url('server.company', '21100', 'DRS011MI', 'Lst', '?EDES=AAA&PREX=6')
    'http://server.company:21100/m3api-rest/execute/DRS011MI/Lst?EDES=AAA&PREX=6'

    >>> create_url('server.company', '21100', 'DRS011MI', 'Dlt', ';max_recs=0;?EDES=AAA&PREX=6')
    'http://server.company:21100/m3api-rest/execute/DRS011MI/Dlt;max_recs=0;?EDES=AAA&PREX=6'
    '''

    return f'http://{ip}:{port}/m3api-rest/execute/{program}/{transaction}{params}'


def execute(url: str, usr: str, pwd: str) -> requests.models.Response:
    '''Returns a request for the given url, user and password.'''
    request = requests.get(
        url,
        verify=False,
        auth=HTTPBasicAuth(usr, pwd),
    )

    return request


class Api:
    '''A wrapper class for call the API in a more convinient way. Just
    initialize the class with the ip, port, user and password. Then
    use the request function with the program, transaction and **kwargs
    to get the response object from the API call.'''

    def __init__(self, ip: int, port: str, usr: str, pwd: str):
        self.ip = ip
        self.port = port
        self.usr = usr
        self.pwd = pwd

    def request(self, program: str, transaction: str, **kwargs) -> requests.models.Response:
        ''' Make an API request. Note the the **kwargs represents the possible
        input fields for the API, ususally the column names. Refer to documenation
        for the specific API. If max_recs is passed the maximum number of return
        rows will be modified. Note that if 0 is given as max_recs, all records
        will be retured.

        Examples of usage:
        >> api = Api('server.company', 21000, 'a_username', 'a_password')
        >> request = api.request('MMS005MI', 'SelRoute', max_recs=0, EDES='AAA')

        Calling request object will return the request status.
        Calling request.content will return the XML returned from the API as
        a string object that can be parsed with a XML library.
        '''

        param_str = dict_to_param_str(kwargs)
        url = create_url(self.ip, self.port, program, transaction, param_str)
        response = execute(url, self.usr, self.pwd)
        response.close()

        return response
