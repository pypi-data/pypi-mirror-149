from numpy import exp, pi
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from ....definitions import config_dict
from ....Functions.init_fig import init_fig
from ....Functions.labels import decode_label, HOLEM_LAB, LAM_LAB

PATCH_COLOR = config_dict["PLOT"]["COLOR_DICT"]["PATCH_COLOR"]
MAGNET_COLOR = config_dict["PLOT"]["COLOR_DICT"]["MAGNET_COLOR"]
ROTOR_COLOR = config_dict["PLOT"]["COLOR_DICT"]["ROTOR_COLOR"]
STATOR_COLOR = config_dict["PLOT"]["COLOR_DICT"]["STATOR_COLOR"]
VENT_COLOR = config_dict["PLOT"]["COLOR_DICT"]["VENT_COLOR"]
VENT_EDGE = config_dict["PLOT"]["COLOR_DICT"]["VENT_EDGE"]


def plot(
    self,
    fig=None,
    ax=None,
    is_lam_only=False,
    sym=1,
    alpha=0,
    delta=0,
    is_edge_only=False,
    edgecolor=None,
    is_add_arrow=False,
    is_show_fig=True,
    win_title=None,
):
    """Plot a Lamination with Buried Magnets in a matplotlib fig

    Parameters
    ----------
    self : LamHole
        A LamHole object
    fig : Matplotlib.figure.Figure
        existing figure to use if None create a new one
    ax : Matplotlib.axes.Axes object
        Axis on which to plot the data
    is_lam_only: bool
        True to plot only the lamination (remove the magnets)
    sym : int
        Symmetry factor (1= plot full machine, 2= half of the machine...)
    alpha : float
        angle for rotation (Default value = 0) [rad]
    delta : complex
        complex for translation (Default value = 0)
    is_edge_only: bool
        To plot transparent Patches
    edgecolor:
        Color of the edges if is_edge_only=True
    is_add_arrow : bool
        To add an arrow for the magnetization
    is_show_fig : bool
        To call show at the end of the method
    win_title : str
        Window title

    Returns
    -------
    fig : Matplotlib.figure.Figure
        Figure containing the plot
    ax : Matplotlib.axes.Axes object
        Axis containing the plot
    """

    # Lamination bore
    if self.is_stator:
        Lam_Name = "Stator"
        lam_color = STATOR_COLOR
    else:
        Lam_Name = "Rotor"
        lam_color = ROTOR_COLOR

    # List of surface to plot the lamination
    surf_list = self.build_geometry(sym=sym, alpha=alpha, delta=delta)
    patches = list()
    for surf in surf_list:
        label_dict = decode_label(surf.label)
        if LAM_LAB in label_dict["surf_type"]:
            patches.extend(
                surf.get_patches(
                    color=lam_color, is_edge_only=is_edge_only, edgecolor=edgecolor
                )
            )
        elif HOLEM_LAB in label_dict["surf_type"] and not is_lam_only:
            patches.extend(
                surf.get_patches(
                    color=MAGNET_COLOR, is_edge_only=is_edge_only, edgecolor=edgecolor
                )
            )
        elif surf.label is not None and "Ventilation_" in surf.label:
            patches.extend(
                surf.get_patches(
                    color=VENT_COLOR, edgecolor=edgecolor, is_edge_only=is_edge_only
                )
            )
        else:
            patches.extend(
                surf.get_patches(is_edge_only=is_edge_only, edgecolor=edgecolor)
            )

    (fig, ax, patch_leg, label_leg) = init_fig(fig=fig, ax=ax, shape="rectangle")

    ax.set_xlabel("(m)")
    ax.set_ylabel("(m)")

    for patch in patches:
        ax.add_patch(patch)

    # Add Magnetization arrow
    if is_add_arrow:
        for hole in self.hole:
            H = hole.comp_height()
            mag_dict = hole.comp_magnetization_dict()
            for magnet_name, mag_dir in mag_dict.items():
                # Get the correct surface
                mag_surf = None
                mag_id = int(magnet_name.split("_")[-1])
                mag = hole.get_magnet_by_id(mag_id)
                if mag is not None:
                    for surf in hole.build_geometry():
                        label_dict = decode_label(surf.label)
                        if (
                            HOLEM_LAB in label_dict["surf_type"]
                            and label_dict["T_id"] == mag_id
                        ):
                            mag_surf = surf
                            break
                    # Create arrow coordinates
                    Zh = hole.Zh
                    for ii in range(int(Zh / sym)):
                        off = pi if ii % 2 == 1 else 0
                        if mag is not None and mag.type_magnetization == 3:
                            off -= pi / 2
                        Z1 = mag_surf.point_ref * exp(1j * (ii * 2 * pi / Zh + pi / Zh))
                        Z2 = (
                            mag_surf.point_ref + H / 5 * exp(1j * (mag_dir + off))
                        ) * exp(1j * (ii * 2 * pi / Zh + pi / Zh))
                        ax.annotate(
                            text="",
                            xy=(Z2.real, Z2.imag),
                            xytext=(Z1.real, Z1.imag),
                            arrowprops=dict(arrowstyle="->", linewidth=1, color="b"),
                        )

    # Axis Setup
    ax.axis("equal")

    # The Lamination is centered in the figure
    Lim = self.Rext * 1.5
    ax.set_xlim(-Lim, Lim)
    ax.set_ylim(-Lim, Lim)

    # Window title
    if (
        win_title is None
        and self.parent is not None
        and self.parent.name not in [None, ""]
    ):
        win_title = self.parent.name + " " + Lam_Name
    elif win_title is None:
        win_title = Lam_Name
    manager = plt.get_current_fig_manager()
    if manager is not None:
        manager.set_window_title(win_title)

    # Set legend
    if not is_edge_only:
        if self.is_stator:
            patch_leg.append(Patch(color=STATOR_COLOR))
            label_leg.append("Stator")
            ax.set_title("Stator with Interior Magnet")
        else:
            patch_leg.append(Patch(color=ROTOR_COLOR))
            label_leg.append("Rotor")
            ax.set_title("Rotor with Interior Magnet")
        if not is_lam_only:
            patch_leg.append(Patch(color=MAGNET_COLOR))
            label_leg.append("Magnet")
        ax.legend(patch_leg, label_leg)
    if is_show_fig:
        fig.show()
    return fig, ax
