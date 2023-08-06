import typer
import getpass

from . mi_endpoints import mi_endpoint_delete
from . mi_endpoints import mi_endpoint_get
from . mi_endpoints import mi_endpoint_list
from . mi_endpoints import mi_endpoint_save
from . mi_endpoints import mi_endpoint_change_pwd

app = typer.Typer()


@app.command()
def get(name: str):
    endpoint = mi_endpoint_get(name)
    typer.echo(endpoint)


@app.command()
def delete(name: str):
    mi_endpoint_delete(name)
    typer.echo(f'{name} deleted!')


@app.command()
def save(name: str, ip: str, port: int, usr: str):
    pwd = getpass.getpass(f'Enter password for {name}: ')
    mi_endpoint_save(name, ip, port, usr, pwd)
    typer.echo(f'Saved {name}!')


@app.command()
def list():
    for row in mi_endpoint_list():
        typer.echo(row)

@app.command()
def set_pwd(name: str):
    if name in [row.name for row in mi_endpoint_list()]:
        pwd = getpass.getpass(f'Input new password for {name}: ')
        mi_endpoint_change_pwd(name, pwd)
        typer.echo(f'Password for {name} changed!')

    else:
        typer.echo(f'Endpoint {name} is not configured!')

if __name__ == '__main__':
    app()