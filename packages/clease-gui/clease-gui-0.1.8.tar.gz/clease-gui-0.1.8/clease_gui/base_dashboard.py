from abc import ABC, abstractmethod
from pathlib import PurePath
import clease
from clease_gui.style_mixin import WidgetStyleMixin
from clease_gui.app_data import AppDataKeys, AppData
from clease_gui.event_context import EventContextManager, log_error

__all__ = ["BaseDashboard"]


class BaseDashboard(WidgetStyleMixin, ABC):
    def __init__(self, app_data: AppData, initialize=True):
        """Base class for dashboards.

        :param app_data: Dictionary with application data, which will be passed around
            to all dashboards, and possibly widgets if they need them.
        :param initialize: Bool, toggle whether the ``initialize`` function is called.
            Mainly useful for testing purposes. Should generally be set to True.
        """
        # We make app_data a property, as to protect it, so it's not changed into
        # a new object. Can still be mutated.
        if not isinstance(app_data, AppData):
            raise TypeError(f"Expected AppData type, got {app_data!r}")
        self._app_data = app_data
        # Create access to the constant app data keys through ".KEYS.<some-key>"
        self.KEYS = AppDataKeys
        if initialize:
            self.initialize()

    @property
    def app_data(self) -> AppData:
        """Return the app data"""
        return self._app_data

    def get_cwd(self):
        return self.app_data[self.KEYS.CWD]

    @property
    def dev_mode(self) -> bool:
        """Are we in developer mode?"""
        return self.app_data.get(self.KEYS.DEV_MODE, False)

    @property
    def debug(self) -> bool:
        """Alternative name for dev mode"""
        return self.dev_mode

    def log_error(self, logger, *args, **kwargs) -> None:
        """Log as exception if we're in dev mode, otherwise only log as error"""
        log_error(*args, logger=logger, dev_mode=self.dev_mode, **kwargs)

    def event_context(self, logger=None) -> EventContextManager:
        """Context where events which shouldn't
        crash the GUI even on an exception are run"""
        return EventContextManager(logger=logger, dev_mode=self.dev_mode)

    @abstractmethod
    def initialize(self) -> None:
        """Initialize any widgets related to the dashboard"""

    @abstractmethod
    def display(self) -> None:
        """Display the dashboard"""

    @property
    def settings(self) -> clease.settings.ClusterExpansionSettings:
        """Short-cut for accessing settings, since this is a common operation.
        Raises a KeyError if it doesn't exist."""
        try:
            return self.app_data[self.KEYS.SETTINGS]
        except KeyError:
            # Raise a better message
            raise KeyError("No settings present. Create/load a settings object first.") from None

    def get_db_name(self) -> PurePath:
        """Return the DB name form the settings, and prepend the current
        working directory"""
        settings = self.settings
        cwd = self.app_data[self.KEYS.CWD]
        return cwd / settings.db_name
