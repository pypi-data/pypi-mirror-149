import os
import click
from .main_cli import clease_gui_cli

__all__ = ["launch"]


def _build_cmd(args, notebook):
    if notebook:
        cmd = "jupyter notebook"
    else:
        cmd = "jupyter-lab"
    if args:
        joined = " ".join(args)
        cmd = f"{cmd} {joined}"
    return cmd


@clease_gui_cli.command()
@click.option(
    "-n",
    "--notebook",
    is_flag=True,
    help="""
Use Jupyter notebook instead of Jupyter lab?.""",
)
@click.argument("args", nargs=-1)
def launch(args, notebook):
    cmd = _build_cmd(args, notebook)
    os.system(cmd)
