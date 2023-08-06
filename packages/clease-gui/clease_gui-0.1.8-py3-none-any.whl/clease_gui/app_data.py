import logging
from collections import defaultdict
from typing import Dict, Any, Callable
from enum import Enum, IntEnum, auto
from pathlib import Path
import attr
from clease import jsonio
from clease_gui.logging_widget import register_logger

__all__ = ["save_app_data", "load_app_data", "AppDataKeys"]

logger = logging.getLogger(__name__)
register_logger(logger)


class AppDataKeys(str, Enum):
    """Collection of keys which (may) be in the app_data.
    Keys starting with an '_' will not be saved in the app state."""

    # "private" keys
    CWD = "_cwd"
    STATUS = "_status"
    DEV_MODE = "_dev_mode"
    STEP_OBSERVER = "_mc_step_obs"

    # Regular app data keys
    SUPERCELL = "supercell"
    SETTINGS = "settings"
    ECI = "eci"
    CANONICAL_MC_DATA = "canonical_mc_data"

    # The evaluator cannot be saved to file, so save it as private
    # instance of an Evaluate class
    EVALUATE = "_evaluator"

    @classmethod
    def is_key_private(cls, key: str) -> bool:
        """Check if a given key is considered 'private'"""
        return key.startswith("_")

    @classmethod
    def is_key_public(cls, key: str) -> bool:
        """Check if a given key is considered 'public'"""
        return not cls.is_key_private(key)

    @classmethod
    def iter_public_keys(cls):
        yield from filter(cls.is_key_public, cls)

    @classmethod
    def iter_private_keys(cls):
        yield from filter(cls.is_key_private, cls)


class Notifier(IntEnum):
    """Type of notification"""

    SET = auto()
    DELETE = auto()
    POP = auto()


@attr.define
class Notification:
    """A notification that something changed in the AppData"""

    key: str = attr.field()
    old_value: Any = attr.field()
    new_value: Any = attr.field()
    notifier: Notifier = attr.field()


class AppData(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Shortcut to AppDataKeys
        self.app_keys = AppDataKeys
        self._subscribers = defaultdict(list)

    def subscribe(self, key: str, func: Callable[[Notification], None]) -> None:
        self._subscribers[key].append(func)

    def notify_subscribers(self, key: str, change: Notification) -> None:
        for ii, func in enumerate(self._subscribers[key]):
            logger.debug("Notifying subscriber %d to key %s from %s", ii, key, change.notifier)
            func(change)

    def pop(self, key: str, **kwargs) -> Any:
        """Pop an item like in dict.pop(), and then notify anyone who subscribes to that key.
        Notificattion only occurs after the delete."""
        old_value = self.get(key, None)
        ret_val = super().pop(key, **kwargs)
        change = Notification(key, old_value, None, Notifier.POP)
        self.notify_subscribers(key, change)
        return ret_val

    def __setitem__(self, key: str, value: Any) -> None:
        """Change an item, and then notify anyone who subscribes to that key.
        Notificattion only occurs after the set."""
        old_value = self.get(key, None)
        ret_val = super().__setitem__(key, value)
        change = Notification(key, old_value, value, Notifier.SET)
        self.notify_subscribers(key, change)
        return ret_val

    def __delitem__(self, key: str) -> None:
        """Delete an item, and then notify anyone who subscribes to that key.
        Notificattion only occurs after the delete."""
        old_value = self.get(key, None)
        ret_val = super().__delitem__(key)
        change = Notification(key, old_value, None, Notifier.DELETE)
        self.notify_subscribers(key, change)
        return ret_val


def save_app_data(app_data: Dict[str, Any], fname) -> None:
    fname = Path(fname)
    data = app_data.copy()
    to_remove = []
    for key in data:
        # Find keys which we don't want to save
        # Any keys starting with a "_" we say
        # we don't want to save
        if AppDataKeys.is_key_private(key):
            to_remove.append(key)
    for key in to_remove:
        data.pop(key, None)

    with fname.open("w") as file:
        jsonio.write_json(file, data)


def load_app_data(fname) -> AppData:
    fname = Path(fname)
    with fname.open() as file:
        return AppData(**jsonio.read_json(file))
