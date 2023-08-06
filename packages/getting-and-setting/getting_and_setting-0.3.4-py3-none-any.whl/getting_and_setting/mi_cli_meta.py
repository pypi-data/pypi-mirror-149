import typer

from typing import List

from . import MiApi

from . mi_endpoints import mi_endpoint_get

app = typer.Typer(help='Fetch metadata')


@app.command()
def transaction(endpoint: str, program: str, transaction: str):
    endpoint = mi_endpoint_get(endpoint)
    
    api = MiApi(endpoint.host, endpoint.port, endpoint.usr, endpoint.pwd)
    records = api.transaction_meta(program, transaction)

    typer.echo(records)


@app.command()
def program(endpoint: str, program: str):
    endpoint = mi_endpoint_get(endpoint)
    
    api = MiApi(endpoint.host, endpoint.port, endpoint.usr, endpoint.pwd)
    records = api.program_meta(program)

    typer.echo(records)



@app.command()
def list():
    endpoint = mi_endpoint_get(endpoint)
    
    api = MiApi(endpoint.host, endpoint.port, endpoint.usr, endpoint.pwd)
    records = api.program_list()

    typer.echo(records)