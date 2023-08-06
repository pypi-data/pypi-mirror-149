import logging
from clease_gui import register_logger

base_logger = logging.getLogger(__name__)
register_logger(base_logger)

__all__ = ["log_error", "EventContextManager"]


def log_error(*args, logger=None, dev_mode=False, **kwargs) -> None:
    """Log an error, and determine logging level based on whether we are in dev mode or not.
    I.e., in dev_mode the traceback is included, but not in regular mode."""
    logger = logger or base_logger
    fnc = logger.exception if dev_mode else logger.error
    fnc(*args, **kwargs)


class EventContextManager:
    """Context manager for an event which shouldn't cause a crash of the GUI,
    such as when clicking a button, but an expected file is not found.
    The error will be logged, and the class can be inspected after the context
    to see if an error was found (and which type).

    Will catch any "Exception", but not "BaseException".

    Example:
    with EventContextManager() as cm:
        raise ValueError()
    assert cm.success is False
    assert isinstance(cm.exc_value, ValueError)
    """

    def __init__(self, dev_mode=False, logger=None):
        self.had_error = False
        # Record exception type and values
        self.exc_type = None
        self.exc_value = None

        self.is_done = False
        self._dev_mode = dev_mode
        self._logger = logger

    def __enter__(self):
        base_logger.debug("Entering event context.")
        return self

    def __exit__(self, exc_type, exc_value, trace) -> bool:
        self.exc_type = exc_type
        self.exc_value = exc_value
        if exc_type is not None:
            # We had an error. Log and suppress
            self.had_error = True
            log_error(exc_value, logger=self._logger, dev_mode=self._dev_mode)
        base_logger.debug("Leaving event context. Error detected? %s", self.had_error)
        self.is_done = True
        # Suppress any exception which is of type "Exception",
        # similar to except Exception: in a try/except block
        # i.e. we don't won't to block BaseExceptions such as KeyboardInterrupt or SystemExit
        return isinstance(exc_value, Exception)

    @property
    def success(self) -> bool:
        """Are we done, and completed with no error?"""
        return self.is_done and not self.had_error
