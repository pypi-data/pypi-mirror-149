import typer

from typing import List

from . import MiApi

from . mi_endpoints import mi_endpoint_get

from . mi_models import MiRecords
from . mi_models import MiError
from . mi_models import Status

app = typer.Typer(help='Interact with the API')

@app.command()
def execute(endpoint: str, program: str, transaction: str, params: List[str]):
    try:
        params =  {
            f'{row.split("=")[0]}': row.split('=')[1]
            for row in params
        }
    except:
        typer.echo(f'Failed to parse extra parameters!\n {params}\n Has to have format KEY=VALUE')
        return
    
    endpoint = mi_endpoint_get(endpoint)
    
    api = MiApi(endpoint.host, endpoint.port, endpoint.usr, endpoint.pwd)
    records = api.execute(program, transaction, **params)

    typer.echo(records)
