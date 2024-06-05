#!/usr/bin/python3

import pytest
from datetime import timezone
from . import WatersmartClient

pytest_plugins = ("pytest_asyncio",)


def test_amend_with_local_ts():
    datapoint = {
        "read_datetime": 1717488000,
        "gallons": 67.2,
        "flags": None,
        "leak_gallons": 0,
    }
    result = WatersmartClient._amend_with_local_ts(datapoint, tzinfo=timezone.utc)
    assert result["read_datetime"] == datapoint["read_datetime"]
    assert result["gallons"] == datapoint["gallons"]
    assert result["leak_gallons"] == datapoint["leak_gallons"]
    assert result["flags"] == datapoint["flags"]
    assert "local_datetime" not in datapoint
    assert "local_datetime" in result
    assert f"{result["local_datetime"]}" == "2024-06-04 01:00:00+00:00"


@pytest.mark.asyncio
async def test_disallow_non_watersmart_urls():
    with pytest.raises(AssertionError):
        WatersmartClient("https://wsmart.example", "e@mail", "passw4rd")
