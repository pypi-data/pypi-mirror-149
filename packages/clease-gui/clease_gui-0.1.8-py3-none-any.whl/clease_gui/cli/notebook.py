"""Open a Jupyter notebook"""

import click
import shutil
from pathlib import Path, PurePath
from clease_gui.utils import get_assets_path
from .main_cli import clease_gui_cli

__all__ = []

DEFAULT_FILENAME = "clease_gui.ipynb"


def copy_default_notebook(filename: PurePath) -> None:
    src = get_assets_path() / "default_notebook.ipynb"
    if filename.exists():
        raise RuntimeError(f"File {filename} already exists.")
    shutil.copy(src, filename)


@clease_gui_cli.command()
@click.option(
    "-f",
    "--filename",
    type=str,
    default=DEFAULT_FILENAME,
    required=False,
    help=f"""
Create a new notebook to be used with the CLEASE GUI.
Defaults to "{DEFAULT_FILENAME}".""",
)
def new(filename: str) -> None:
    """Create a mew notebook to be used with the CLEASE GUI."""
    file_path = Path(filename)
    # Ensure we're making an .ipynb file
    file_path = file_path.with_suffix(".ipynb")
    if file_path.exists():
        click.echo(f'File "{file_path}" already exists.')
        return
    click.echo(f"Creating new notebook: {file_path}")
    copy_default_notebook(file_path)
