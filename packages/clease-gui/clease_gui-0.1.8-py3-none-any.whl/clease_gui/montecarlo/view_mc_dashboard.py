import logging

import threading
from IPython.display import display, clear_output
import ipywidgets as widgets
from clease.montecarlo.observers import MoveObserver

from clease_gui import register_logger, utils
from clease_gui.base_dashboard import BaseDashboard
from clease_gui.status_bar import update_statusbar

import nglview as nv

from .mc_nglviewer import MCNGLDisplay

__all__ = ["MCViewDashboard"]

logger = logging.getLogger(__name__)
register_logger(logger)


class MCViewDashboard(BaseDashboard):
    def initialize(self) -> None:
        self.viewer = MCNGLDisplay()

        self.center_btn = utils.make_clickable_button(self._center_click, description="Center")
        self.update_btn = utils.make_clickable_button(self._update_click, description="Update")
        self.play_mc = utils.make_clickable_button(self._play_mc_click, description="Play")
        self.stop_movie_btn = utils.make_clickable_button(self._stop_mc_click, description="Stop")
        self.steps_per_frame = widgets.BoundedIntText(
            min=1,
            max=999999,
            step=1,
            value=10,
            description="Steps per frame",
            **self.DEFAULT_STYLE_KWARGS,
        )
        self.time_per_frame = widgets.BoundedFloatText(
            min=0.1,
            max=99,
            step=0.1,
            description="Time per frame (s)",
            value=0.2,
            **self.DEFAULT_STYLE_KWARGS,
        )
        self.movie_progress = widgets.IntProgress()
        self.movie_progress_label = widgets.Label()

        self.viewer_out = widgets.Output()
        self._event = threading.Event()

        with self.viewer_out:
            clear_output()
            display(self.viewer.viewer.display(gui=False))

    def get_move_obs(self) -> MoveObserver:
        obs = self.app_data.get(self.KEYS.STEP_OBSERVER, None)
        if obs is None:
            raise ValueError(
                "No MC movie has been made yet. "
                "Enable step recording in the 'Observe Steps' box "
                "on the MC page."
            )
        return obs

    def _stop_mc_click(self, b):
        self._event.set()

    def _center_click(self, b):
        self.get_ngl_widget().center()

    def display(self) -> None:
        experimental_label = widgets.Label("Note: This is still experimental")
        experimental_label.value += "\n"
        display(experimental_label)
        display(self.center_btn)
        box = widgets.HBox(children=[self.update_btn, self.steps_per_frame, self.time_per_frame])
        display(box)
        box = widgets.HBox(children=[self.play_mc, self.stop_movie_btn])
        display(box)
        box = widgets.HBox(children=[self.movie_progress, self.movie_progress_label])
        display(box)
        display(self.viewer_out)

    def handle_resize(self) -> None:
        self.get_ngl_widget().handle_resize()

    def get_ngl_widget(self) -> nv.NGLWidget:
        """Get the NGL widget object"""
        return self.viewer.viewer

    @update_statusbar
    def _play_mc_click(self, b):
        with self.event_context(logger=logger):
            self._play_mc_in_thread()

    @utils.disable_cls_widget("update_btn")
    def _update_click(self, b):
        with self.event_context(logger=logger):
            self._update()

    def _update(self):
        """Construct a new NGL widget, and re-draw it"""
        move_obs = self.get_move_obs()
        self.viewer.make_viewer(move_obs.base_atoms)
        self.draw_viewer()

    def draw_viewer(self):
        """Redraw the MC Viewer widget"""
        with self.viewer_out:
            clear_output(wait=True)
            self.viewer.display()

    def _play_mc_in_thread(self):
        self.get_move_obs()  # Ensure the move observer exists

        # Remake the viewer
        thread_draw = threading.Thread(target=self._update, daemon=True)
        thread_draw.start()
        thread_draw.join()
        # Start the movie
        thread = threading.Thread(target=self._play_mc, daemon=True)
        thread.start()

    @utils.disable_cls_widget("play_mc")
    @utils.disable_cls_widget("update_btn")
    def _play_mc(self):
        """Start the movie"""
        move_obs = self.get_move_obs()
        self._event.clear()

        logger.info("Playing movie")
        tot = len(move_obs.steps)
        self.movie_progress.max = tot
        self.movie_progress.value = 0

        def _do_update(ii, atoms):
            self.movie_progress.value = ii
            self.movie_progress_label.value = f"{ii}/{tot}"
            self.viewer.replace_structure(atoms)

        # for ii, step in enumerate(move_obs.steps, start=1):
        for ii, atoms in enumerate(move_obs.reconstruct_iter(), start=1):
            if self._event.is_set():
                logger.info("Stopping movie.")
                self.movie_progress_label.value += ", interrupted."
                break
            if ii % self.steps_per_frame.value == 0:
                _do_update(ii, atoms)
                # Slight delay per frame
                self._event.wait(self.time_per_frame.value)
        else:
            # Movie done, no interrupt.
            # Do a final update
            _do_update(ii, atoms)
            self.movie_progress_label.value += ", done!"
            logger.info("Movie complete.")
