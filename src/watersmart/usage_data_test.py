#!/usr/bin/python3

import pytest
import os
import time

from . import WatersmartClient

pytest_plugins = ("pytest_asyncio",)


def _assert_amend_with_local_ts():
    datapoint = {
        "read_datetime": 1717488000,
        "gallons": 67.2,
        "flags": None,
        "leak_gallons": 0,
    }
    result = WatersmartClient._amend_with_local_ts(datapoint)
    assert result["read_datetime"] == datapoint["read_datetime"]
    assert result["gallons"] == datapoint["gallons"]
    assert result["leak_gallons"] == datapoint["leak_gallons"]
    assert result["flags"] == datapoint["flags"]
    assert "local_datetime" not in datapoint
    assert "local_datetime" in result
    assert f"{result['local_datetime']}" == "2024-06-04 08:00:00"


def test_amend_with_local_ts_in_local():
    _assert_amend_with_local_ts()


def test_amend_with_local_ts_in_pacific():
    os.environ["TZ"] = "America/Los_Angeles"
    time.tzset()
    _assert_amend_with_local_ts()


def test_amend_with_local_ts_in_utc():
    os.environ["TZ"] = "utc"
    time.tzset()
    _assert_amend_with_local_ts()


@pytest.mark.asyncio
async def test_disallow_non_watersmart_urls():
    with pytest.raises(AssertionError):
        WatersmartClient(
            url="https://wsmart.example", email="e@mail", password="passw4rd"
        )
