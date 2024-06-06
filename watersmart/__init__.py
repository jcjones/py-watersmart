"""Main WaterSmart module"""

import logging
import time

from aiohttp_client_cache import CachedSession, SQLiteBackend
from importlib.metadata import version


class WatersmartClient:
    def __init__(self, url, email, password):
        self._url = url
        self._email = email
        self._password = password
        self._headers = {"User-Agent": "py-watersmart " + version("py-watersmart")}
        self._cache = SQLiteBackend(
            expire_after=60 * 60 * 6,
            include_headers=False,
            cache_name="~/.cache/py-watersmart.db",
        )
        self._session = CachedSession(
            cache=self._cache,
            headers=self._headers,
        )
        self._data_series = []
        assert "watersmart.com" in url, "Exepcted a watersmart.com URL"
        logging.debug("WatersmartClient ready, headers: %s", self._headers)

    async def _login(self):
        url = f"https://{self._url}/index.php/welcome/login?forceEmail=1"
        login = {"token": "", "email": self._email, "password": self._password}
        await self._session.post(url, data=login)

    async def _populate_data(self):
        url = f"https://{self._url}/index.php/rest/v1/Chart/RealTimeChart"
        chart_rsp = await self._session.get(url)
        data = await chart_rsp.json()
        self._data_series = data["data"]["series"]

    @classmethod
    def _amend_with_local_ts(cls, datapoint):
        # The read_datetime is a timestamp in local TZ, not UTC, which
        # confuses python datetime, so use the naive struct_time
        ts = time.gmtime(datapoint["read_datetime"])
        result = datapoint.copy()
        result["local_datetime"] = time.strftime("%Y-%m-%d %H:%M:%S", ts)
        return result

    async def usage(self):
        if not self._data_series:
            logging.debug("Loading watersmart data")
            await self._login()
            await self._populate_data()
            await self._close()

        result = []

        for datapoint in self._data_series:
            result.append(WatersmartClient._amend_with_local_ts(datapoint))

        return result

    async def _close(self):
        await self._session.close()
