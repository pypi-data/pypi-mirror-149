from collections import namedtuple
from contextlib import contextmanager
import functools
import ipywidgets as widgets
from IPython.display import display

from clease_gui.base_dashboard import BaseDashboard
import clease_gui.colors as colors

__all__ = ["StatusBar", "update_statusbar"]

UpdatableWidget = namedtuple("UpdatableWidget", "widget, update_function")


def update_statusbar(func):
    """Decorator to update statusbar after function completion, and mark
    status as busy from a dashboard object."""

    @functools.wraps(func)
    def _wrapper(self, *args, **kwargs):
        try:
            statusbar: StatusBar = self.app_data[self.KEYS.STATUS]["statusbar"]
        except KeyError:
            # Something happened, we couldn't get the statusbar
            return func(self, *args, **kwargs)

        # Set statusbar as busy
        with statusbar.status_busy():
            return_val = func(self, *args, **kwargs)
        return return_val

    return _wrapper


class StatusBar(BaseDashboard):
    IS_BUSY = "is_busy"

    def __init__(self, *args, **kwargs):
        self._processes = 0
        self.all_widgets = {}
        super().__init__(*args, **kwargs)
        # Register this statusbar in the app data
        # So others can register it as busy
        self.app_data[self.KEYS.STATUS] = {"statusbar": self}
        self._subscribe()

    def _subscribe(self) -> None:
        """Subscribe the status widgets to the app data"""

        def _wrapper(fnc):
            def _dec(change):
                return fnc()

            return _dec

        # Wrap the updater, since it doesn't care about the notification.
        wrapped = _wrapper(self.update_all)
        for key in [self.KEYS.SETTINGS, self.KEYS.ECI, self.KEYS.SUPERCELL]:
            self.app_data.subscribe(key, wrapped)

    def initialize(self):
        # Create widgets
        self.status_widget = widgets.HTML(value=self.is_busy_str())
        self.register_status_widget(self.IS_BUSY, self.status_widget, self.is_busy_str)

        self.has_settings_wdgt = widgets.Label(value=self.has_settings())
        self.register_status_widget("settings", self.has_settings_wdgt, self.has_settings)

        self.has_eci_wdgt = widgets.Label(value=self.has_eci())
        self.register_status_widget("eci", self.has_eci_wdgt, self.has_eci)

        self.has_supercell_widget = widgets.Label(value=self.has_supercell())
        self.register_status_widget("supercell", self.has_supercell_widget, self.has_supercell)

    def display(self):
        hbox1 = widgets.VBox(
            children=[
                self.status_widget,
                self.has_settings_wdgt,
            ],
            # Add a bit of margin to the right
            layout=widgets.Layout(margin="0 50px 0 0"),
        )

        hbox2 = widgets.VBox(
            children=[
                self.has_eci_wdgt,
                self.has_supercell_widget,
            ]
        )

        boxes = widgets.HBox(children=[hbox1, hbox2], layout=widgets.Layout(border="solid 1px"))

        display(boxes)

    def register_status_widget(self, name, widget, func):
        updatable = UpdatableWidget(widget, func)
        self.all_widgets[name] = updatable

    @property
    def processes(self):
        return self._processes

    def has_supercell(self):
        val = self.key_available(self.KEYS.SUPERCELL)
        return self._format_bool("Supercell available?", val)

    def is_busy(self):
        return self.processes > 0

    def is_busy_str(self):
        s = "Status:   "
        if self.is_busy() > 0:
            # status = Colors.latex_red('Busy')
            status = colors.Colors.html_color("Busy", "red")
        else:
            status = colors.Colors.html_color("Idle", "green")
        return f"{s} {status}"

    def has_settings(self):
        val = self.key_available(self.KEYS.SETTINGS)
        return self._format_bool("Settings available?", val)

    def has_eci(self):
        val = self.key_available(self.KEYS.ECI)
        return self._format_bool("ECI available?", val)

    def key_available(self, key: str) -> bool:
        """A key is considered missing if it is either None or
        doesn't exist in the app data."""
        return self.app_data.get(key, None) is not None

    def _format_bool(self, s, boolean):
        val = colors.bool2symbol[boolean]
        return f"{s}   {val}"

    def update_all(self):
        for updatable_widget in self.all_widgets.values():
            func = updatable_widget.update_function
            updatable_widget.widget.value = func()

    def update_status(self):
        widget = self.all_widgets[self.IS_BUSY]
        func = widget.update_function
        widget.widget.value = func()

    def increment_process(self) -> None:
        self._processes += 1

    def deincrement_process(self) -> None:
        if self._processes < 1:
            raise RuntimeError("Should not be deincrementing process which is less than 1")
        self._processes -= 1

    @contextmanager
    def status_busy(self):
        self.increment_process()
        try:
            self.update_status()
            yield
        finally:
            self.deincrement_process()
            self.update_status()

    def __repr__(self):
        return f"{self.__class__.__name__}(busy={self.is_busy()}, processes={self.processes})"
