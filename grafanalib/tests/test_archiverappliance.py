"""Tests for the EPICS Archiver Appliance Datasource."""
import pytest

from grafanalib import core
from grafanalib import archiverappliance as arch
from grafanalib import _gen
from io import StringIO


def test_graph_to_json():
    graph = core.Graph(
        title="Archiver test graph",
        dataSource="EPICS Archiver",
        targets=[
            arch.ArchiverTargetQuery(
                target="MFX:DG1:MMS:01.RBV",
                refId="A",
                functions=[arch.transform_scale(2.0)],
            ),
        ],
        lines=True,
        lineWidth=1,
        yAxes=core.YAxes(
            core.YAxis(format=core.NO_FORMAT),
        ),
        gridPos=core.GridPos(h=8, w=12, x=0, y=0),
    )

    stream = StringIO()
    _gen.write_dashboard(graph, stream)
    assert stream.getvalue() != ""


@pytest.mark.parametrize(
    "func, args, expected",
    [
        pytest.param(
            arch.transform_scale, ["abc"], ValueError, id="transform_scale_float_str"
        ),
        pytest.param(arch.transform_scale, ["abc"], ValueError, id="transform_scale-0"),
        pytest.param(arch.transform_moving_average, ["def"], ValueError, id="transform_moving_average"),
        pytest.param(arch.array_to_scalar_by_average, ["foobar"], ValueError, id="array_to_scalar_by_average"),
        pytest.param(arch.options_disable_auto_raw, ["FALSE"], ValueError, id="options_disable_auto_raw"),
        pytest.param(arch.options_disable_extrapolation, [0], ValueError, id="options_disable_extrapolation"),
    ],
)
def test_function_with_bad_args(func, args, expected):
    with pytest.raises(expected):
        func(*args)


@pytest.mark.parametrize(
    "func, args",
    [
        pytest.param(arch.transform_scale, [0.0], id="transform_scale-0.0"),
        pytest.param(arch.transform_scale, [0], id="transform_scale-0"),
        pytest.param(arch.transform_offset, [0], id="transform_offset"),
        pytest.param(arch.transform_delta, [], id="transform_delta"),
        pytest.param(arch.transform_fluctuation, [], id="transform_fluctuation"),
        pytest.param(arch.transform_moving_average, [1], id="transform_moving_average"),
        pytest.param(arch.array_to_scalar_by_average, [], id="array_to_scalar_by_average"),
        pytest.param(arch.array_to_scalar_by_max, [], id="array_to_scalar_by_max"),
        pytest.param(arch.array_to_scalar_by_min, [], id="array_to_scalar_by_min"),
        pytest.param(arch.array_to_scalar_by_sum, [], id="array_to_scalar_by_sum"),
        pytest.param(arch.array_to_scalar_by_median, [], id="array_to_scalar_by_median"),
        pytest.param(arch.array_to_scalar_by_std, [], id="array_to_scalar_by_std"),
        pytest.param(arch.filter_top, [5, "avg"], id="filter_top"),
        pytest.param(arch.filter_bottom, [3, "avg"], id="filter_bottom"),
        pytest.param(arch.filter_exclude, ["pattern"], id="filter_exclude"),
        pytest.param(arch.sort_by_average, ["asc"], id="sort_by_average"),
        pytest.param(arch.sort_by_max, ["asc"], id="sort_by_max"),
        pytest.param(arch.sort_by_min, ["asc"], id="sort_by_min"),
        pytest.param(arch.sort_by_sum, ["asc"], id="sort_by_sum"),
        pytest.param(arch.sort_by_abs_max, ["asc"], id="sort_by_abs_max"),
        pytest.param(arch.sort_by_abs_min, ["asc"], id="sort_by_abs_min"),
        pytest.param(arch.options_max_num_pvs, [10], id="options_max_num_pvs"),
        pytest.param(arch.options_bin_interval, [10], id="options_bin_interval"),
        pytest.param(arch.options_disable_auto_raw, [True], id="options_disable_auto_raw"),
        pytest.param(arch.options_disable_extrapolation, ["false"], id="options_disable_extrapolation"),
    ],
)
def test_function_with_good_args(func, args):
    # Does not raise after validation:
    func(*args)
