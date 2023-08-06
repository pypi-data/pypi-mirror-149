import logging
from IPython.display import display, clear_output
import ipywidgets as widgets

from clease_gui import utils, register_logger
from clease_gui.base_dashboard import BaseDashboard
from clease_gui.status_bar import update_statusbar

__all__ = ["ClusterDashboard"]

logger = logging.getLogger(__name__)
register_logger(logger)


class ClusterDashboard(BaseDashboard):
    """Dashboard for printing and visualizing the available clusters/figures
    in the active settings object."""

    def initialize(self) -> None:
        # Output for displaying clusters table
        self.clusters_content_out = widgets.Output(
            layout=dict(
                overflow="auto",
                width="100%",
                height="350px",
            )
        )

        self.refresh_table_button = utils.make_clickable_button(
            self._on_refresh_table_click, description="Update Clusters Table"
        )

        self.view_clusters_button = utils.make_clickable_button(
            self._on_view_clusters_click, description="View Clusters"
        )

    def display(self) -> None:
        button_box = widgets.HBox(children=[self.refresh_table_button, self.view_clusters_button])
        display(button_box, self.clusters_content_out)

    @utils.disable_cls_widget("refresh_table_button")
    @update_statusbar
    def _on_refresh_table_click(self, b) -> None:
        """Event handler for when refresh table button is clicked."""
        with self.event_context(logger=logger):
            logger.info("Updating cluster table.")
            self.refresh_clusters_table()

    def refresh_clusters_table(self) -> None:
        """Draw the clusters table in the clusters content outputs"""
        settings = self.settings
        with self.clusters_content_out:
            clear_output(wait=True)

            # This call will trigger calculating the cluster list if it doesn't exist
            n_clusters = len(self.settings.cluster_list)
            print(f"Number of clusters: {n_clusters:d}")
            print(settings.clusters_table())

    @utils.disable_cls_widget("view_clusters_button")
    @update_statusbar
    def _on_view_clusters_click(self, b) -> None:
        """Event handler when view clusters button is clicked."""
        logger.info("Temporarily disabled.")
        return
        with self.event_context(logger=logger):
            logger.info("Opening clusters in the ASE GUI")
            self.view_clusters()

    def view_clusters(self) -> None:
        """Visualize the clusters in the ASE GUI"""
        self.settings.view_clusters()
