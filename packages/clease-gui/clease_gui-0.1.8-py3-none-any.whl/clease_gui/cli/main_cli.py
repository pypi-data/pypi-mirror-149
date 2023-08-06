import click
from clease_gui import __version__

__all__ = ["clease_gui_cli"]


@click.group()
@click.version_option(__version__)
def clease_gui_cli():
    """The main CLEASE GUI CLI"""
