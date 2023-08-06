import os
import json
import warnings
from inspect import currentframe
from sympy.external import import_module

appdirs = import_module(
    'appdirs',
    min_module_version='1.4.4')

appname = "spb"
cfg_file = "config.json"
cfg_dir = appdirs.user_data_dir(appname)
os.makedirs(cfg_dir, exist_ok=True)
file_path = os.path.join(cfg_dir, cfg_file)


def _hardcoded_defaults():
    # Hardcoded default values
    return dict(
        # Find more Plotly themes at the following page:
        # https://plotly.com/python/templates/
        plotly={
            "theme": "seaborn",
            "grid": True,
            "use_latex": False,
        },
        # Find more Bokeh themes at the following page:
        # https://docs.bokeh.org/en/latest/docs/reference/themes.html
        bokeh={
            "theme": "caliber",
            "sizing_mode": "stretch_width",
            "update_event": True,
            "grid": True,
            "show_minor_grid": True,
            "minor_grid_line_alpha": 0.6,
            "minor_grid_line_dash": [2, 2],
            "use_latex": False,
        },
        k3d={
            "bg_color": 0xFFFFFF,       # 3620427
            "grid_color": 0xE6E6E6,     # 0x888888
            "label_color": 0x444444,    # 0xDDDDDD
            "grid": True,
            "use_latex": True,
        },
        matplotlib={
            "axis_center": None,  # "auto", "center"
            "grid": True,
            "show_minor_grid": True,
            "use_latex": True,
        },
        backend_2D="matplotlib",
        backend_3D="matplotlib",
        complex={
            "modules": None,     # "mpmath"
            "coloring": "a"
        },
        interactive={
            "use_latex": True,
            "throttled": False
        },
        plot3d={
            "use_cm": False
        },
        adaptive={
            "goal": 0.01
        },
        plot_range={
            "min": -10,
            "max": 10
        }
    )


def get_default_settings():
    """Return the default setting dictionary for inspection.

    Examples
    ========

    Visualize the default settings.

        >>> from spb.defaults import get_default_settings
        >>> print(get_default_settings)
    """
    return _hardcoded_defaults()


def reset():
    """Restore original settings."""
    set_defaults(_hardcoded_defaults())


def _load_settings():
    """Load settings and inject the names into the current namespace."""
    mergedeep = import_module('mergedeep')
    merge = mergedeep.merge

    frame = currentframe()

    cfg = dict()
    if os.path.exists(file_path):
        with open(file_path) as f:
            cfg = json.load(f)

    default_cfg = _hardcoded_defaults()

    # Because the user can directly change the configuration file, we need
    # to assure that all the necessary options are present (maybe, the user
    # deleted something accidentally)
    cfg = merge({}, default_cfg, cfg)
    frame.f_globals["cfg"] = cfg

    # check that the chosen backends are available
    backends_2D = ["plotly", "bokeh", "matplotlib"]
    backends_3D = ["plotly", "matplotlib", "k3d"]

    def check_backend(k, backends):
        if cfg[k] not in backends:
            # restore hardcoded values in order to be able to load the module
            # the next time
            reset()

            raise ValueError(
                "`{}` must be one of the following ".format(k)
                + "values: {}\n".format(backends)
                + "Received: = '{}'\n".format(cfg[k])
                + "Reset config file to hardcoded default values: done."
            )

    check_backend("backend_2D", backends_2D)
    check_backend("backend_3D", backends_3D)

    # load the selected backends
    if cfg["backend_2D"] == "plotly":
        from spb.backends.plotly import PlotlyBackend as TWO_D_B
    elif cfg["backend_2D"] == "bokeh":
        from spb.backends.bokeh import BokehBackend as TWO_D_B
    elif cfg["backend_2D"] == "matplotlib":
        from spb.backends.matplotlib import MatplotlibBackend as TWO_D_B
    elif cfg["backend_2D"] == "k3d":
        from spb.backends.k3d import K3DBackend as TWO_D_B

    if cfg["backend_2D"] == cfg["backend_3D"]:
        THREE_D_B = TWO_D_B
    else:
        if cfg["backend_3D"] == "plotly":
            from spb.backends.plotly import PlotlyBackend as THREE_D_B
        elif cfg["backend_3D"] == "matplotlib":
            from spb.backends.matplotlib import MatplotlibBackend as THREE_D_B
        elif cfg["backend_3D"] == "k3d":
            from spb.backends.k3d import K3DBackend as THREE_D_B

    frame.f_globals["TWO_D_B"] = TWO_D_B
    frame.f_globals["THREE_D_B"] = THREE_D_B


def set_defaults(cfg):
    """Set the default options for the plotting backends and save them to
    a file.

    Parameters
    ==========
    cfg : dict
        Dictionary containing the new values

    Examples
    ========

    Change the default 2D plotting backend to MatplotlibBackend.

        >>> from spb.defaults import cfg, set_defaults
        >>> ## to visualize the current settings
        >>> # print(cfg)
        >>> cfg["backend_2D"] = "matplotlib"
        >>> set_defaults(cfg)

    Notes
    =====

    This plotting module uses the `appdir` module [#fn1]_ to determine the
    best location where to save the settings. It will save a human readable
    `config.json` file, which SHOULD NOT be modified directly with a text
    editor.
    Use the ``set_defaults`` function to modify the configuration settings!

    References
    ==========

    .. [#fn1] https://github.com/ActiveState/appdirs

    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=4)
        warnings.warn("Successfully written settings to {}".format(file_path))

    _load_settings()


_load_settings()
