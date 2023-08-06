import logging
from IPython.display import display, clear_output
import ipywidgets as widgets
from clease_gui import register_logger
from clease_gui.base_dashboard import BaseDashboard
from . import CanonicalMC, PlotMCDashboard, MCRunDashboard, MCViewDashboard

__all__ = ["MainMCDashboard"]

logger = logging.getLogger(__name__)
register_logger(logger)


class MainMCDashboard(BaseDashboard):
    def initialize(self):
        self.canonical_mc_out = widgets.Output()
        self.canonical_mc_dashboard = CanonicalMC(self.app_data)
        with self.canonical_mc_out:
            self.canonical_mc_dashboard.display()

        self.plot_out = widgets.Output(layout={"height": "100%"})
        self.plot_dashboard = PlotMCDashboard(self.app_data)
        with self.plot_out:
            self.plot_dashboard.display()

        self.store_mc_run_out = widgets.Output()
        self.store_mc_dashboard = MCRunDashboard(self.app_data)
        with self.store_mc_run_out:
            self.store_mc_dashboard.display()

        self.view_mc_out = widgets.Output()
        self.view_mc_dashboard = MCViewDashboard(self.app_data)
        with self.view_mc_out:
            clear_output()
            self.view_mc_dashboard.display()

        self.tab = widgets.Tab(
            children=[
                self.canonical_mc_out,
                self.plot_out,
                self.store_mc_run_out,
                self.view_mc_out,
            ]
        )

        self.tab.set_title(0, "Canonical MC")
        self.tab.set_title(1, "Plotting")
        self.tab.set_title(2, "MC Runs")
        self.tab.set_title(3, "View MC")

        # A fix for showing the viewer in a tab.
        # Code adapted from aiida.
        # https://github.com/aiidalab/aiidalab-qe/issues/69
        def on_selected_index_change(change):
            index = change["new"]
            # Accessing the viewer only if the corresponding tab is present.
            # i.e. only trigger the toggling if we open the View MC tab.
            if self.tab._titles[str(index)] == "View MC":
                self.view_mc_dashboard.handle_resize()
                viewer = self.view_mc_dashboard.get_ngl_widget()

                def toggle_camera():
                    """Toggle camera between perspective and orthographic."""
                    viewer.camera = (
                        "perspective" if viewer.camera == "orthographic" else "orthographic"
                    )

                toggle_camera()
                toggle_camera()

        self.tab.observe(on_selected_index_change, "selected_index")

    def display(self):
        display(self.tab)
