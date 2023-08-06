import logging
import random
import time
from collections import Counter
from typing import Tuple, Dict, List, Callable, Sequence
from IPython.display import display, clear_output
import ipywidgets as widgets
import ase
import ase.io
import clease
from clease_gui.base_dashboard import BaseDashboard
from clease_gui.status_bar import update_statusbar
from clease_gui.colors import bool2symbol
from clease_gui import register_logger, utils

__all__ = ["SupercellDashboard"]

logger = logging.getLogger(__name__)
register_logger(logger)


class SupercellDashboard(BaseDashboard):
    def initialize(self):

        self.sc_widgets = []
        for coord in ("x", "y", "z"):
            wdgt = widgets.BoundedIntText(
                description=f"Repetition ({coord}):",
                value=5,
                min=1,
                max=999,
                **self.DEFAULT_STYLE_KWARGS,
            )
            self.sc_widgets.append(wdgt)

        self.make_atoms_btn = widgets.Button(
            description="Make random supercell", layout=self.DEFAULT_BUTTON_LAYOUT
        )
        self.make_atoms_btn.on_click(self._on_make_supercell_click)

        self.desc_label = widgets.Label(value=self.make_desc_label())

        self.view_atoms_btn = utils.make_clickable_button(
            self._on_view_atoms_click,
            description="View Current Supercell",
            layout=self.DEFAULT_BUTTON_LAYOUT,
        )

        self.load_supercell_button = widgets.Button(description="Load Supercell")
        self.load_supercell_text = widgets.Text(description="Filename:", value="supercell.traj")
        self.load_supercell_button.on_click(self._on_load_supercell_click)

        self.save_supercell_button = widgets.Button(description="Save Supercell")
        self.save_supercell_text = widgets.Text(description="Filename:", value="supercell.traj")
        self.save_supercell_button.on_click(self._on_save_supercell_click)

        self.species_output = widgets.Output()
        self.species_output.clear_output()

    def display(self):
        display(self.desc_label)
        vbox_sc_widgets = widgets.VBox(children=self.sc_widgets)

        hbox_buttons = widgets.HBox(
            children=[
                self.make_atoms_btn,
                self.view_atoms_btn,
            ]
        )

        load_hbox = widgets.HBox(children=[self.load_supercell_button, self.load_supercell_text])
        save_hbox = widgets.HBox(children=[self.save_supercell_button, self.save_supercell_text])
        display(save_hbox, load_hbox)
        display(hbox_buttons)
        display(vbox_sc_widgets)
        display(self.species_output)

    def sc_formula_unit(self):
        try:
            supercell = self.supercell
        except ValueError:
            return ""
        else:
            return supercell.get_chemical_formula()

    @update_statusbar
    @utils.disable_cls_widget("load_supercell_button")
    def _on_load_supercell_click(self, b):
        with self.event_context(logger=logger):
            self.load_supercell()

    def load_supercell(self):
        fname = self.load_supercell_text.value
        if fname == "":
            raise ValueError("No filename supplied")
        cwd = self.app_data[self.KEYS.CWD]
        fname = cwd / fname
        self._load_supercell(fname)

    def _load_supercell(self, fname):
        logger.info("Loading supercell from file: %s", fname)
        atoms = ase.io.read(fname)
        self.set_supercell(atoms)
        logger.info("Load successful.")

    def make_random_supercell(self):
        atoms = self.settings.prim_cell.copy()
        atoms *= self.repetitions

        self.settings.set_active_template(atoms)
        nib = [len(x) for x in self.settings.index_by_basis]
        x = self.concentration.get_random_concentration(nib)
        supercell = self._make_atoms_at_conc(x)
        self.set_supercell(supercell)

    @update_statusbar
    @utils.disable_cls_widget("view_atoms_btn")
    def _on_view_atoms_click(self, b):
        with self.event_context(logger=logger):
            self._visualize_supercell()
            self._update_desc_label()

    def _visualize_supercell(self):
        supercell = self.supercell
        if supercell is None:
            raise ValueError("No supercell has been made yet.")
        gui = utils.make_ase_gui(supercell)
        gui.run()
        logger.info("Opened supercell in a new ASE GUI window.")

    def make_desc_label(self):
        text = "Create a supercell."
        try:
            sc = self.supercell
        except ValueError:
            # No supercell present, just return initial text part
            return text
        formula_unit = sc.get_chemical_formula()
        ntot = len(sc)

        text += f" Current formula unit: {formula_unit}."
        text += f" Total number of atoms: {ntot}"

        return text

    def _update_desc_label(self):
        self.desc_label.value = self.make_desc_label()

    def set_supercell(self, atoms: ase.Atoms, draw_species_output=True):
        # XXX: Do we want to set the active template here?
        self.settings.set_active_template(atoms)
        self.app_data[self.KEYS.SUPERCELL] = atoms
        self._update_desc_label()
        if draw_species_output:
            self._make_species_output()

    @property
    def supercell(self):
        try:
            return self.app_data[self.KEYS.SUPERCELL]
        except KeyError:
            raise ValueError("No supercell available in app data.")

    @property
    def repetitions(self) -> Tuple[int]:
        return tuple(wdgt.value for wdgt in self.sc_widgets)

    @update_statusbar
    @utils.disable_cls_widget("make_atoms_btn")
    def _on_make_supercell_click(self, b):
        with self.event_context(logger=logger):
            start_time = time.perf_counter()
            self.make_random_supercell()
            dt = time.perf_counter() - start_time
            logger.info("Supercell created in %.3f s.", dt)

    def _get_new_struct_obj(self):
        """Helper function for creating a NewStructures object"""
        return clease.structgen.NewStructures(self.settings)

    @property
    def concentration(self):
        return self.settings.concentration

    def _make_atoms_at_conc(self, x):
        new_struct = self._get_new_struct_obj()
        num_atoms_in_basis = [len(indices) for indices in self.settings.index_by_basis]
        num_to_insert = self.concentration.conc_in_int(num_atoms_in_basis, x)
        return new_struct._random_struct_at_conc(num_to_insert)

    def save_supercell(self):
        supercell = self.supercell
        fname = self.save_supercell_text.value
        if fname == "":
            raise ValueError("No filename supplied.")
        fname = self.app_data[self.KEYS.CWD] / fname
        logger.info("Saving supercell to file: %s", fname)
        ase.io.write(fname, supercell)
        logger.info("Save successful.")

    @update_statusbar
    @utils.disable_cls_widget("save_supercell_button")
    def _on_save_supercell_click(self, b):
        with self.event_context(logger=logger):
            self.save_supercell()

    def get_species_per_basis(self) -> List[Dict[str, int]]:
        settings = self.settings
        supercell = self.supercell

        idx_by_basis = settings.index_by_basis

        species_per_basis = []
        for idx in idx_by_basis:
            atoms = supercell[idx]
            species = Counter(atoms.symbols)
            species_per_basis.append(species)
        return species_per_basis

    def set_supercell_species(self, species_per_basis: Sequence[Dict[str, int]]):
        # Check that all species per basis add up to the correct number
        # by comparing to the current total
        basis_elements = self.settings.basis_elements
        index_by_basis = self.settings.index_by_basis
        for ii, new_basis in enumerate(species_per_basis):
            cur_count = len(index_by_basis[ii])
            new_count = sum(new_basis.values())
            if cur_count != new_count:
                sublatt = ii + 1
                raise ValueError(
                    (
                        "Incorrect number of elements in sublattice {}." " Expected {}, but got {}."
                    ).format(sublatt, cur_count, new_count)
                )
        # Do the update, now we confirmed the counts are OK!
        atoms = self.supercell.copy()
        for ii, indices in enumerate(index_by_basis):
            new_syms = []
            for elem in basis_elements[ii]:
                new_count = species_per_basis[ii].get(elem, 0)
                new_syms.extend([elem] * new_count)
            assert len(new_syms) == len(indices), (len(new_syms), len(indices))
            # Shuffle sublattice
            random.shuffle(new_syms)
            atoms.symbols[indices] = new_syms

        # Check if we violate concentration constraints. We do not update if that's the case.
        if not self.settings.concentration.is_valid(index_by_basis, atoms):
            raise ValueError("The specified configuration violates the concentration constraints.")
        # We don't need to redraw the species output widgets again
        self.set_supercell(atoms, draw_species_output=False)
        logger.info("Supercell updated.")

    def _make_species_output(self):
        out = self.species_output

        species_per_basis = self.get_species_per_basis()

        update_supercell_btn = widgets.Button(description="Update supercell")

        with out:
            clear_output(wait=True)
            get_species_counts = []
            for ii, species_count in enumerate(species_per_basis):
                sublattice_index = ii + 1
                # Draw the sublattice boxes, and add the callback so we can get number of species
                output, callback = make_sublattice_box(species_count, sublattice_index)
                get_species_counts.append(callback)
                display(output)

            display(update_supercell_btn)

        def make_species_per_basis():
            count = []
            for callback in get_species_counts:
                count_in_sublattice = callback()
                count.append(count_in_sublattice)
            return count

        def on_update_click(b):
            with utils.disable_widget_context(update_supercell_btn):
                with self.event_context(logger=logger):
                    self.set_supercell_species(make_species_per_basis())

        update_supercell_btn.on_click(on_update_click)


def make_sublattice_box(
    species_count: Dict[str, int], sublattice_index: int
) -> Tuple[widgets.Output, Callable[[], Dict[str, int]]]:
    """Draw a box for the sublattice containing a given set of species.
    Returns the Output object with the boxes, as well as a function
    with the counts of the species specified by the user in the boxes in
    that sublattice."""
    # total number of species in the sublattice
    tot_in_basis = sum(species_count.values())

    # The output object in which the boxes are going to be drawn
    sublattice_out = widgets.Output(layout={"border": "1px solid lightgray"})

    def make_make_label_text(is_ok=True):
        s = f"Sublattice {sublattice_index}  {bool2symbol[is_ok]}"
        return f"<h1 style='font-size:17px'> {s} </h1>"

    label = widgets.HTML(value=make_make_label_text())
    # Let's draw the label text on top
    with sublattice_out:
        clear_output()
        display(label)

    # List with all the elemental count boxes
    all_elem_boxes = []
    # A list of species according to the order in all_elem_boxes
    species_lst: List[str] = []

    # A box with the total count
    tot_box = widgets.IntText(
        description="Total in basis:",
        value=tot_in_basis,
        disabled=True,
        style={"description_width": "initial"},
    )
    # Box with the total specified number in this basis
    tot_specified = widgets.IntText(
        description="Total specified:",
        value=0,
        disabled=True,
        style={"description_width": "initial"},
    )
    # Group the "total" boxes horizontally
    tot_hbox = widgets.HBox(children=[tot_box, tot_specified])

    def update():
        """Callback which updates the tot_specified box and the label"""
        new_tot = sum(widget.value for widget in all_elem_boxes)
        tot_specified.value = new_tot
        label.value = make_make_label_text(new_tot == tot_in_basis)

    def observe_change(change):
        """Has the total number of assigned species has changed?"""
        if utils.is_value_change(change):
            update()

    # Create the individual species boxes
    with sublattice_out:
        for species, count in species_count.items():
            wdgt, ratio_wdgt = _make_species_boxes(species, count, tot_in_basis)
            # We need to update tot_specified if we make a change here
            wdgt.observe(observe_change)
            species_lst.append(species)
            all_elem_boxes.append(wdgt)
            hbox = widgets.HBox(children=[wdgt, ratio_wdgt])
            # Draw the count boxes 1-by-1
            display(hbox)

        # Finally, draw the "total" boxes
        display(tot_hbox)
    # Update the count after we made the individual species boxes
    update()

    def get_counts() -> Dict[str, int]:
        """Get the counts of the widgets created by this function.

        Raises a value error if the counts are inconsistent."""
        counts = {}
        for species, wdgt in zip(species_lst, all_elem_boxes):
            value = wdgt.value
            counts[species] = value
        cur_count = sum(counts.values())
        if cur_count != tot_in_basis:
            raise ValueError(
                (
                    "Incorrect number of elements in sublattice {}." " Expected {}, but got {}."
                ).format(sublattice_index, tot_in_basis, cur_count)
            )
        return counts

    return sublattice_out, get_counts


def _make_species_boxes(
    species: str, count: int, tot_in_basis: int
) -> Tuple[widgets.BoundedIntText, widgets.FloatText]:
    """Helper function to make the species count widget and the corresponding ratio box."""
    # The box in which the user types in the species count
    wdgt = widgets.BoundedIntText(value=count, min=0, max=tot_in_basis, description=f"{species}:")
    # A box with the ratio of species this corresponds to
    ratio_wdgt = widgets.FloatText(
        value=count / tot_in_basis,
        description="Ratio:",
        disabled=True,
    )

    def count_changed(change):
        if utils.is_value_change(change):
            ratio_wdgt.value = change.new / tot_in_basis

    wdgt.observe(count_changed)

    return wdgt, ratio_wdgt
