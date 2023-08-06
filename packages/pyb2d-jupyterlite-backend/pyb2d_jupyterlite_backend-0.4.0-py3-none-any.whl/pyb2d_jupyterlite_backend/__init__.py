from .plot import render_world, plot_world, animate_world
import sys
import types
import b2d


def mock_plot():
    plot = sys.modules["b2d.plot"] = types.ModuleType("plot")
    plot.render_world = render_world
    plot.plot_world = plot_world
    plot.animate_world = animate_world
    b2d.plot = plot


ALL_MOCKS = [mock_plot]


def apply_mocks():
    """Apply all of the mocks needed for mainstream packages to work, if possible"""
    import warnings

    for mock in ALL_MOCKS:
        try:
            mock()
        except Exception as err:
            warnings.warn("failed to apply mock", mock, err)


apply_mocks()
