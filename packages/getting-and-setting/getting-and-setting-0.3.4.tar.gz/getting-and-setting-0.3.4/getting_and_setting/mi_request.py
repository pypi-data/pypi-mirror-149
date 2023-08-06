''' mi_api.py
A module to that makes calles to the Infor ION API simple. This moduele
handels url creation, authentication and requests. Reconmended way to use
this moduel is by using the class Api.

Author: Kim Timothy Engh
Email: kim.timothy.engh@epiroc.com
Licence: GPLv3 '''


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

    maxrecs = f';maxrecs={param_dict.pop("maxrecs")};' if param_dict.get("maxrecs") != None else ''

    params_str = r'&'.join(
        [
            f'{key}={value}'
            for key, value
            in param_dict.items()
        ]
    )

    return f'{maxrecs}?{params_str}'


def mi_request(url: str, usr: str, pwd: str) -> requests.models.Response:
    request = requests.get(
        url,
        verify=False,
        auth=HTTPBasicAuth(usr, pwd),
    )
    request.close()

    return request


def mi_request_metadata(host: str, port: int, usr: str, pwd: str, program: str) -> requests.models.Request:
    url = f'http://{host}:{port}/m3api-rest/metadata/{program}'
    request = mi_request(url, usr, pwd)

    return request

def mi_request_programs(host: str, port: int, usr: str, pwd: str) -> requests.models.Request:
    url = f'http://{host}:{port}/m3api-rest/metadata'
    request = mi_request(url, usr, pwd)

    return request

def mi_request_execute(host: str, port: int, usr: str, pwd:str, program: str, transaction: str, **kwargs) -> requests.models.Response:
    param_str = dict_to_param_str(kwargs)
    url = f'http://{host}:{port}/m3api-rest/execute/{program}/{transaction}{param_str}'
    request = mi_request(url, usr, pwd)

    return request
