"""Main WaterSmart module"""

import aiohttp


class WatersmartClient:
    def __init__(self, url, email, password):
        self._url = url
        self._email = email
        self._password = password
        self._session = aiohttp.ClientSession(
            headers={"User-Agent": "py-watersmart 0.0.0"}
        )
        self._data_series = []

    async def _login(self):
        url = f"https://{self._url}/index.php/welcome/login?forceEmail=1"
        login = {"token": "", "email": self._email, "password": self._password}
        await self._session.post(url, data=login)

    async def _populate_data(self):
        url = f"https://{self._url}/index.php/rest/v1/Chart/RealTimeChart"
        chart_rsp = await self._session.get(url)
        data = await chart_rsp.json()
        self._data_series = data["data"]["series"]

    async def usage(self):
        if not self._data_series:
            await self._login()
            await self._populate_data()
            await self._close()

        return self._data_series

    async def _close(self):
        await self._session.close()
