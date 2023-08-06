from typing import Sequence, Union
import logging
import functools
from pathlib import Path, PurePath
from contextlib import contextmanager
from ipywidgets import DOMWidget
import ipywidgets as widgets
from ase import Atoms
from clease_gui.logging_widget import register_logger

__all__ = [
    "is_value_change",
    "disable_widget_context",
    "disables_widget",
    "disable_cls_widget",
    "make_clickable_button",
    "get_assets_path",
    "make_ase_gui",
]

logger = logging.getLogger(__name__)
register_logger(logger)


def get_assets_path() -> PurePath:
    """Return the path to the assets directory"""
    return Path(__file__).parent / "assets"


def make_clickable_button(*click_event, description="", **button_kwargs) -> widgets.Button:
    """Helper function for making a new button and adding 1 or more callback
    functions on click events.
    Combines the general pattern of

    button = widgets.Button(**kwargs)
    button.on_click(my_event)

    into a single function call.
    """
    button = widgets.Button(description=description, **button_kwargs)
    for callback in click_event:
        button.on_click(callback)
    return button


def is_value_change(change: dict) -> bool:
    """Determine if a widget change is due to a change in value.
    This change comes from the widget.observe() function.
    """
    return change["type"] == "change" and change["name"] == "value"


@contextmanager
def disable_widget_context(widget: DOMWidget):
    """Context manager which temporarily disables a widget.
    Usage:

    with disable_widget_context(my_widget):
        do_stuff()
    """
    if not isinstance(widget, DOMWidget):
        raise TypeError(f"Widget must be of type DOMWidget, got {type(widget)}")
    # Get the current state of the widget
    prev_state: bool = widget.disabled
    widget.disabled = True
    logger.debug("Widget disabled: %s", widget.disabled)
    try:
        yield
    finally:
        # Enable the widget again, if it was previously enabled.
        widget.disabled = prev_state
        logger.debug("Widget restored, new state: %s", widget.disabled)


def disables_widget(widget):
    """Decorator which disables a widget while function is executing.
    Usage:
    @disables_widget(my_widget)
    def my_func():
        # While this function is executing, the widget "my_widget" is disabled.
        do_stuff()
    """

    def decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            with disable_widget_context(widget):
                return func(*args, **kwargs)

        return _wrapper

    return decorator


def disable_cls_widget(widget_name: str):
    """Decorator which disables a widget of a class which is a member of "self"
    Assumes the widget name exists in "self", i.e. it uses getattr(self, widget_name)
    to access the widget.

    @disable_cls_widget('my_widget_name')
    def my_func(self):
        do_stuff()
    """

    def decorator(func):
        @functools.wraps(func)
        def _wrapper(self, *args, **kwargs):
            # Find the widget to be disabled.
            widget = getattr(self, widget_name)
            # Disable the widget during function execution.
            with disable_widget_context(widget):
                return func(self, *args, **kwargs)

        return _wrapper

    return decorator


def make_ase_gui(images: Union[Sequence[Atoms], Atoms], expr="", **kwargs):
    """Helper function to create a new ASE gui instance.
    The expr="" default ensures that no matplotlib figure objects are constructed by default.

    Does not run the gui! That has to be explicitly called by the runner, e.g. by

    gui = make_ase_gui(my_image)
    gui.run()
    """
    # Delay the GUI import, this fails in the conda-forge pipeline
    from ase.gui.gui import GUI
    from ase.gui.images import Images

    if isinstance(images, Atoms):
        # if it's not a single atoms object, assume it's multiple
        images = [images]
    im_obj = Images(images=images)
    gui = GUI(images=im_obj, expr=expr, **kwargs)
    return gui
