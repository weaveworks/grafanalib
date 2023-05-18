"""Tests for elasticsearch."""

import grafanalib.elasticsearch as E
import pytest


def test_rate_metric_agg():
    t = E.RateMetricAgg()
    json_data = t.to_json_data()

    assert json_data["id"] == "0"
    assert json_data["hide"] is False
    assert json_data["field"] == ""
    assert len(json_data["settings"]) == 0
    assert json_data["type"] == "rate"
    assert len(json_data) == 5

    t = E.RateMetricAgg(
        field="some-field",
        hide=True,
        id=2,
        unit="minute",
        mode="sum",
        script="some script"
    )
    json_data = t.to_json_data()

    assert json_data["id"] == "2"
    assert json_data["hide"] is True
    assert json_data["field"] == "some-field"
    assert len(json_data["settings"]) == 3
    assert json_data["settings"]["unit"] == "minute"
    assert json_data["settings"]["mode"] == "sum"
    assert json_data["settings"]["script"] == "some script"
    assert json_data["type"] == "rate"
    assert len(json_data) == 5

    with pytest.raises(ValueError):
        t = E.RateMetricAgg(
            mode="invalid mode"
        )
