from pydoc import describe
import typer

from typing import Optional, List, Tuple

from . import MiApi
from . mi_endpoints import mi_endpoint_get
from . mi_endpoints import mi_endpoint_list

from . import mi_cli_endpoints
from . import mi_cli_api
from . import mi_cli_meta

app = typer.Typer()

app.add_typer(mi_cli_endpoints.app, name='endpoints')
app.add_typer(mi_cli_api.app, name='api')
app.add_typer(mi_cli_meta.app, name='meta')

if __name__ == '__main__':
    app()