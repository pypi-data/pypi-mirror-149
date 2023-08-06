import logging
from IPython.display import display, clear_output
import ipywidgets as widgets
import numpy as np
from clease.settings import ClusterExpansionSettings
from clease_gui import utils
import clease_gui as gui
from clease_gui.app_data import Notification
from clease_gui.base_dashboard import BaseDashboard
from clease_gui.status_bar import update_statusbar

from . import settings_buttons as swidgets

__all__ = ["CESettingsDashboard"]

logger = logging.getLogger(__name__)
gui.register_logger(logger)

DESC_WIDTH = "150px"
STYLE = {"description_width": DESC_WIDTH}


class CESettingsDashboard(BaseDashboard):
    def initialize(self) -> None:
        self.size_mode_out = widgets.Output()
        self.size_mode_widgets = {
            "fixed": swidgets.FixedSizeMode(output=self.size_mode_out),
            "supercell_factor": swidgets.SupercellFactorSizeMode(output=self.size_mode_out),
        }
        self.size_mode_b = widgets.Dropdown(
            options=[("Fixed", "fixed"), ("Supercell Factor", "supercell_factor")],
            value="supercell_factor",
            description="Size mode:",
            **self.DEFAULT_STYLE_KWARGS,
        )
        self.size_mode_b.observe(self._on_size_mode_change)

        # Common settings, such as max cluster dia, background atoms and database name
        self.out_common = widgets.Output()
        self.common_settings_widget = swidgets.CommonSettingsButtons(
            self.app_data, output=self.out_common
        )
        self.common_settings_widget.display_widgets()

        self.update_settings_btn = utils.make_clickable_button(
            self._on_update_settings_click, description="Update Settings"
        )
        self.app_data.subscribe(self.KEYS.SETTINGS, self._enable_settings_button)

    def _enable_settings_button(self, change: Notification):
        if change.key == self.KEYS.SETTINGS:
            # Enable button depending if we have a settings
            is_disabled = change.new_value is None
            self.update_settings_btn.disabled = is_disabled

    @update_statusbar
    @utils.disable_cls_widget("update_settings_btn")
    def _on_update_settings_click(self, b):
        with self.event_context(logger=logger):
            self.update_settings()
            logger.info("Updated settings.")

    def update_settings(self) -> None:
        """Update the CE settings of the internal settings object (if it exists)."""
        # Fetch the live settings object (if it exists)
        settings = self.settings
        kwargs = self.get_settings_kwargs(updatable=True)
        for key, value in kwargs.items():
            setattr(settings, key, value)
        # We explicitly clear the cache, just for safety.
        # XXX: Should eventually be done in CLEASE itself,
        # it seems like this doesn't happen upon adjusting the MCD.
        settings.clear_cache()

    def display(self) -> None:
        super().display()
        display(self.out_common)

        # Buttons for size mode
        with self.size_mode_out:
            self.active_size_mode_widget.display_widgets()
        display(self.size_mode_b, self.size_mode_out)
        display(self.update_settings_btn)

    @property
    def active_size_mode(self):
        return self.size_mode_b.value

    @property
    def active_size_mode_widget(self):
        return self.size_mode_widgets[self.active_size_mode]

    def _on_size_mode_change(self, change):
        if utils.is_value_change(change):
            self._update_size_mode_widget()

    def _update_size_mode_widget(self):
        logger.debug("Updating active size mode widget")
        with self.size_mode_out:
            clear_output(wait=True)
            self.active_size_mode_widget.display_widgets()

    def get_settings_kwargs(self, updatable: bool = False):
        """Get the kwargs for settings. If updatable=True, only
        get the settings which may be updated."""
        size_kwargs = self.active_size_mode_widget.value
        common_settings_kwargs = self.common_settings_widget.value
        kwargs = dict(
            **common_settings_kwargs,
            **size_kwargs,
        )
        if updatable:
            # Remove any kwargs which may not be updated.
            # TODO: Lock this button, so it cannot be changed when a settings exists
            kwargs.pop("include_background_atoms", None)
        return kwargs

    def set_widgets_from_load(self, settings: ClusterExpansionSettings) -> None:
        self._load_settings(settings)

    def _load_settings(self, settings: ClusterExpansionSettings):
        # Guess the size mode
        if settings.size is None:
            logger.debug("Detected supercell factor mode")
            # use supercell factor
            self.size_mode_b.value = "supercell_factor"
            self._update_size_mode_widget()
            scf = settings.supercell_factor
            skew = settings.skew_threshold
            self.active_size_mode_widget.set_widget_value("supercell_factor", scf)
            self.active_size_mode_widget.set_widget_value("skew_threshold", skew)
        else:
            logger.debug("Detected fixed size mode")
            self.size_mode_b.value = "fixed"
            # self._update_size_mode_widget()
            logger.debug("Getting size value")
            value = settings.size  # in 3x3 matrix
            # Use diagonal
            value = np.diag(value)
            value = ", ".join(map(str, value))
            logger.debug("Setting widget %s to value %s", "size", value)
            self.active_size_mode_widget.set_widget_value("size", value)

        # Settings stored directly in the settings object
        all_keys = (
            "basis_func_type",
            "db_name",
            "max_cluster_size",
            "max_cluster_dia",
            "include_background_atoms",
        )
        for key in all_keys:
            value = get_value_for_widget(settings, key)
            logger.debug("Setting %s to %s", key, value)
            self.common_settings_widget.set_widget_value(key, value)


def get_value_for_widget(settings, key):
    """Get a value from the settings, and sanitize it for settings
    a widget state"""
    if key == "basis_func_type":
        return settings.basis_func_type.name
    if key in {
        "db_name",
        "max_cluster_size",
        "max_cluster_dia",
        "include_background_atoms",
    }:
        return getattr(settings, key)

    raise ValueError(f"Cannot deal with key: {key}")
