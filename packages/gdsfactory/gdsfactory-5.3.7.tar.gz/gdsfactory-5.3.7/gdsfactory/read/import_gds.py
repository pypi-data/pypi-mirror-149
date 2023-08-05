from functools import lru_cache
from pathlib import Path
from typing import Callable, Optional, Union, cast

import gdspy
import numpy as np
from omegaconf import OmegaConf
from phidl.device_layout import CellArray, DeviceReference

from gdsfactory.cell import CACHE
from gdsfactory.component import Component
from gdsfactory.config import CONFIG, logger
from gdsfactory.name import get_name_short
from gdsfactory.snap import snap_to_grid


@lru_cache(maxsize=None)
def import_gds(
    gdspath: Union[str, Path],
    cellname: Optional[str] = None,
    flatten: bool = False,
    snap_to_grid_nm: Optional[int] = None,
    name: Optional[str] = None,
    decorator: Optional[Callable] = None,
    gdsdir: Optional[Union[str, Path]] = None,
    safe_cell_names: bool = False,
    **kwargs,
) -> Component:
    """Returns a Componenent from a GDS file.

    Adapted from phidl/geometry.py

    if any cell names are found on the component CACHE we append a $ with a
    number to the name

    Args:
        gdspath: path of GDS file.
        cellname: cell of the name to import (None) imports top cell.
        flatten: if True returns flattened (no hierarchy)
        snap_to_grid_nm: snap to different nm grid (does not snap if False)
        name: Optional name. Over-rides the default imported name.
        decorator: function to apply over the imported gds.
        gdsdir: optional GDS directory.
        safe_cell_names: append file hash to imported cell names to avoid
            duplicated cell names.
        kwargs: extra info for the imported component (polarization, wavelength ...).
    """
    gdspath = Path(gdsdir) / Path(gdspath) if gdsdir else Path(gdspath)
    gdshash = gdspy.gdsii_hash(gdspath)
    if not gdspath.exists():
        raise FileNotFoundError(f"No file {gdspath!r} found")

    metadata_filepath = gdspath.with_suffix(".yml")

    gdsii_lib = gdspy.GdsLibrary()
    gdsii_lib.read_gds(str(gdspath))
    top_level_cells = gdsii_lib.top_level()
    cellnames = [c.name for c in top_level_cells]

    if cellname is not None:
        if cellname not in gdsii_lib.cells:
            raise ValueError(
                f"cell {cellname} is not in file {gdspath} with cells {cellnames}"
            )
        topcell = gdsii_lib.cells[cellname]
    elif len(top_level_cells) == 1:
        topcell = top_level_cells[0]
    elif len(top_level_cells) > 1:
        raise ValueError(
            f"import_gds() There are multiple top-level cells in {gdspath!r}, "
            f"you must specify `cellname` to select of one of them among {cellnames}"
        )

    if name:
        if name in CACHE:
            raise ValueError(
                f"name = {name!r} already on cache. "
                "Please, choose a different name or set name = None. "
            )
        else:
            topcell.name = name

    if flatten:
        component = Component(name=name or cellname or cellnames[0])
        polygons = topcell.get_polygons(by_spec=True)
        labels = topcell.get_labels()
        paths = topcell.get_paths()

        for layer_in_gds, polys in polygons.items():
            component.add_polygon(polys, layer=layer_in_gds)
        for label in labels:
            component.add(label)
        for path in paths:
            component.add(path)

        component.name = (
            get_name_short(f"{component.name}_{gdshash}")
            if safe_cell_names
            else get_name_short(component.name)
        )

    else:
        D_list = []
        cell_to_device = {}
        for c in gdsii_lib.cells.values():
            D = Component(name=c.name)
            D.paths = c.paths
            D.polygons = c.polygons
            D.references = c.references
            D.name = c.name
            for label in c.labels:
                rotation = label.rotation
                if rotation is None:
                    rotation = 0
                label_ref = D.add_label(
                    text=label.text,
                    position=np.asfarray(label.position),
                    magnification=label.magnification,
                    rotation=rotation * 180 / np.pi,
                    layer=(label.layer, label.texttype),
                )
                label_ref.anchor = label.anchor

            D.name = (
                get_name_short(f"{D.name}_{gdshash}")
                if safe_cell_names
                else get_name_short(D.name)
            )
            D.unlock()

            cell_to_device[c] = D
            D_list += [D]

        for D in D_list:
            # First convert each reference so it points to the right Device
            converted_references = []
            for e in D.references:
                ref_device = cell_to_device[e.ref_cell]
                if isinstance(e, gdspy.CellReference):
                    dr = DeviceReference(
                        device=ref_device,
                        origin=e.origin,
                        rotation=e.rotation,
                        magnification=e.magnification,
                        x_reflection=e.x_reflection,
                    )
                    dr.owner = D
                    converted_references.append(dr)
                elif isinstance(e, gdspy.CellArray):
                    dr = CellArray(
                        device=ref_device,
                        columns=e.columns,
                        rows=e.rows,
                        spacing=e.spacing,
                        origin=e.origin,
                        rotation=e.rotation,
                        magnification=e.magnification,
                        x_reflection=e.x_reflection,
                    )
                    dr.owner = D
                    converted_references.append(dr)
            D.references = converted_references

            # Next convert each Polygon
            # temp_polygons = list(D.polygons)
            # D.polygons = []
            # for p in temp_polygons:
            #     D.add_polygon(p)

            # Next convert each Polygon
            temp_polygons = list(D.polygons)
            D.polygons = []
            for p in temp_polygons:
                if snap_to_grid_nm:
                    points_on_grid = snap_to_grid(p.polygons[0], nm=snap_to_grid_nm)
                    p = gdspy.Polygon(
                        points_on_grid, layer=p.layers[0], datatype=p.datatypes[0]
                    )
                D.add_polygon(p)
        component = cell_to_device[topcell]
        cast(Component, component)

    name = name or component.name
    component.name = name

    if metadata_filepath.exists():
        logger.info(f"Read YAML metadata from {metadata_filepath}")
        metadata = OmegaConf.load(metadata_filepath)

        for port_name, port in metadata.ports.items():
            if port_name not in component.ports:
                component.add_port(
                    name=port_name,
                    midpoint=port.midpoint,
                    width=port.width,
                    orientation=port.orientation,
                    layer=tuple(port.layer),
                    port_type=port.port_type,
                )

        component.settings = OmegaConf.to_container(metadata.settings)

    component.name = name

    if decorator:
        component_new = decorator(component)
        component = component_new or component
    if flatten:
        component.flatten()
    component.info.update(**kwargs)
    component.lock()
    return component


if __name__ == "__main__":
    gdspath = CONFIG["gdsdir"] / "mzi2x2.gds"
    # c = import_gds(gdspath, snap_to_grid_nm=5, flatten=True, name="TOP")
    c = import_gds(gdspath, snap_to_grid_nm=5, flatten=True)
    print(c)
    c.show()
