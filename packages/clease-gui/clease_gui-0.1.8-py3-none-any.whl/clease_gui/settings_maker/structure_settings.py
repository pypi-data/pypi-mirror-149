import logging
from IPython.display import display
import ipywidgets as widgets

from clease.settings import ClusterExpansionSettings
from clease_gui import utils
from clease_gui.base_dashboard import BaseDashboard
import clease_gui as gui
from . import settings_buttons as swidgets

__all__ = ["StructureSettingsDashboard"]

logger = logging.getLogger(__name__)
gui.register_logger(logger)

DESC_WIDTH = "150px"
STYLE = {"description_width": DESC_WIDTH}


class StructureSettingsDashboard(BaseDashboard):
    """Dashboard related to the structure settings, i.e.
    CEBulk, CECrystal and CESlab
    """

    def initialize(self):
        # Buttons related to the settings type,
        # CEBulk, CECrystal and CESlab

        # Output object for type buttons
        self.out_type = widgets.Output()
        self.out_help = widgets.Output()

        self.type_buttons_dct = {
            "CEBulk": swidgets.CEBulkButtons(self.app_data, output=self.out_type),
            "CECrystal": swidgets.CECrystalButtons(self.app_data, output=self.out_type),
            "CESlab": swidgets.CESlabButtons(self.app_data, output=self.out_type),
        }
        self.type_mode_b = widgets.Dropdown(
            options=[
                ("Bulk", "CEBulk"),
                # Not yet supported
                # ('Crystal', 'CECrystal'),
                # ('Slab', 'CESlab'),
            ],
            description="Type:",
            layout={"width": "max-content"},
            style=STYLE,
        )

        # Add observer to the type, so we know if we need to update the button collection
        def on_type_mode_change(change):
            if utils.is_value_change(change):
                self.update_type_mode()

        self.type_mode_b.observe(on_type_mode_change)

    def update_type_mode(self):
        self.type_buttons.display_widgets()

    @property
    def type_buttons(self):
        mode = self.type_mode_b.value
        return self.type_buttons_dct[mode]

    def display(self):
        super().display()
        display(self.type_mode_b)
        display(self.out_type)
        self.update_type_mode()

    @property
    def type_mode(self):
        return self.type_mode_b.value

    def get_type_kwargs(self):
        return self.type_buttons.value

    def get_settings_kwargs(self):
        kwargs = dict(
            type=self.type_mode,
            **self.get_type_kwargs(),
        )
        return kwargs

    def set_widgets_from_load(self, settings: ClusterExpansionSettings) -> None:
        # Figure out what the builder was
        kwargs = settings.kwargs
        factory = kwargs.get("factory", None)
        if factory != "CEBulk":
            logger.debug("Cannot load settings of factory type: %s", factory)
            return

        # Let's try and load things
        self._load_cebulk_settings(settings)

    def _load_cebulk_settings(self, settings: ClusterExpansionSettings) -> None:
        mode = "CEBulk"
        self.type_mode_b.value = mode
        self.update_type_mode()

        # Get some factory keys
        for key in {"crystalstructure", "a", "c", "c_over_a"}:
            value = settings.kwargs.get(key, None)
            if value is not None:
                self.type_buttons.set_widget_value(key, value)
