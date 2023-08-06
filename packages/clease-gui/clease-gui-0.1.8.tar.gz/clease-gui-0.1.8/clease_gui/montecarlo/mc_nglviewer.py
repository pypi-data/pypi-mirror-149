"""Adaptation of the ASE NGL viewer"""
import logging
from IPython.display import display
import nglview as nv
import ase

from clease_gui import register_logger

logger = logging.getLogger(__name__)
register_logger(logger)


class MCNGLDisplay:
    def __init__(self, xsize=500, ysize=500):
        self.xsize = xsize
        self.ysize = ysize
        self.make_viewer()

    def display(self):
        display(self.viewer)

    def make_viewer(self, atoms: ase.Atoms = None):
        if atoms is not None:
            s = nv.ASEStructure(atoms)
            self.viewer = nv.widget.NGLWidget(s)
        else:
            self.viewer = nv.widget.NGLWidget()
            return
        # Remove the bond cylinders between atoms
        self.viewer.clear_representations()

        self.viewer._set_size(self.xsize, self.ysize)
        self.viewer.camera = "orthographic"

        # self.viewer.add_unitcell()
        self.viewer.add_spacefill()
        self.viewer.update_spacefill(
            radiusType="covalent",
            radiusScale=0.5,
            color_scheme="element",
            color_scale="rainbow",
        )

    def get_orientation(self):
        return self.viewer._camera_orientation

    def replace_structure(self, atoms: ase.Atoms) -> None:
        ngl_traj = nv.ASEStructure(atoms)
        struct = dict(data=ngl_traj.get_structure_string(), ext="pdb")
        self.viewer._remote_call(
            "replaceStructure",
            target="Widget",
            args=[
                struct,
            ],
        )

    def update_coordinates(self, atoms: ase.Atoms) -> None:
        self.viewer.set_coordinates({0: atoms.positions})
