import typer
import getpass
import enum

from typing import Any

from . mi_endpoints import mi_endpoint_delete
from . mi_endpoints import mi_endpoint_get
from . mi_endpoints import mi_endpoint_list
from . mi_endpoints import mi_endpoint_save
from . mi_endpoints import mi_endpoint_change_pwd

from . mi_models import Endpoint

app = typer.Typer(help='Configure Endpoints')


Keys = enum.Enum(
    'Keys',
    {
        field: field
        for field
       in Endpoint.__dataclass_fields__.keys()
    }
)

Names = enum.Enum(
    'Names',
    {
        endpoint.name: endpoint.name
        for endpoint
        in mi_endpoint_list()
    }
)

@app.command()
def get(name: str):
    endpoint = mi_endpoint_get(name)
    typer.echo(endpoint)


@app.command()
def delete(name: str):
    mi_endpoint_delete(name)
    typer.echo(f'{name} deleted!')


@app.command()
def set(name: str, host: str, port: int, usr: str):
    pwd = getpass.getpass(f'Enter password for {name}: ')
    mi_endpoint_save(Endpoint(name, host, port, usr, pwd))
    typer.echo(f'Saved {name}!')


@app.command()
def list():
    for row in mi_endpoint_list():
        typer.echo(row)


@app.command()
def update(name: Names, key: Keys):
    if name not in [row.name for row in mi_endpoint_list()]:
        typer.echo(f'Endpoint {name} is not configured!')
        return

    if key.value == 'pwd':
        value = getpass.getpass(f'Insert new password for {name}: ')
    else:
        value = input(f'Set new {key.value} for {name}: ')

    config = mi_endpoint_get(name)
    setattr(config, key.name, value)

    mi_endpoint_delete(name)
    mi_endpoint_save(config)

    typer.echo(f'Updated {key.value} from {name} to {config.name}!')
        

if __name__ == '__main__':
    app()