"""Define /device endpoints."""
from typing import Awaitable, Callable
import json

from .const import COMMAND_URL, GET_HOME_DEVICES_URL, GET_DEVICE_URL


class Device():  # pylint: disable=too-few-public-methods
    """Define an object to handle the endpoints."""

    def __init__(self, request: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._request: Callable[..., Awaitable] = request

    async def get_devices(self, home_id: str) -> dict:
        """Return device specific data.
        :param home_id: Unique identifier for the device
        :type home_id: ``str``
        :rtype: ``dict``
        """
        devices: dict = await self._request(
            "get",
            GET_HOME_DEVICES_URL % (home_id)
        )

        return devices['data']

    async def get_device_info(self, device_id: str) -> dict:
        """Return device specific data.
        :param home_id: Unique identifier for the device
        :type home_id: ``str``
        :rtype: ``dict``
        """
        device_info: dict = await self._request(
            "get",
            GET_DEVICE_URL % (device_id)
        )

        for items in device_info['data']:
            return items

    async def _set_action(self, dev, user, action: str):
        data = json.dumps({
          "action": action,
          "source": "{\"name\":\"%s\",\"device\":\"%s\"}"
        }) % ((user['firstname']+user['lastname'])[0:7],'apikwikset'[0:7])

        r = await self._request(
            'patch',
            COMMAND_URL % (dev['serialnumber']),
            data=data,
        )
        return r['data']

    async def lock_device(self, dev, user):
        return await self._set_action(dev, user, 'lock')

    async def unlock_device(self, dev, user):
        return await self._set_action(dev, user, 'unlock')