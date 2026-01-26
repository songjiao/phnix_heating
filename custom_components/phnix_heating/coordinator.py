"""Data update coordinator for Phnix Heating integration."""
import logging
from datetime import timedelta
from typing import Any, Dict, List

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .phnix_api import PhnixAPI, PhnixAPIError

_LOGGER = logging.getLogger(__name__)

# Update interval in seconds
UPDATE_INTERVAL = 30


class PhnixDataUpdateCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Coordinator to manage fetching Phnix device data."""

    def __init__(self, hass: HomeAssistant, api: PhnixAPI, device_code: str) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"Phnix Heating ({device_code})",
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self.api = api
        self.device_code = device_code

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from Phnix API.

        Returns a dictionary with:
        - 'raw': The raw data list from API
        - 'by_address': Dict mapping address to data items (for simple lookups)
        - 'by_address_num': Dict mapping (address, num) tuple to data items (for multi-value addresses)
        """
        try:
            _LOGGER.debug("Coordinator fetching device status for %s", self.device_code)
            raw_data: List[Dict[str, Any]] = await self.api.get_device_status()

            # Build lookup indices for efficient entity access
            by_address: Dict[str, Dict[str, Any]] = {}
            by_address_num: Dict[tuple, Dict[str, Any]] = {}

            for item in raw_data:
                address = item.get("address")
                num = item.get("num")

                if address:
                    # Store by address (last one wins if multiple entries)
                    by_address[address] = item

                    # Store by (address, num) for multi-value addresses like 2019, 2034
                    if num:
                        by_address_num[(address, num)] = item

            _LOGGER.debug(
                "Coordinator fetched %d items for %s",
                len(raw_data),
                self.device_code
            )

            return {
                "raw": raw_data,
                "by_address": by_address,
                "by_address_num": by_address_num,
            }

        except PhnixAPIError as err:
            raise UpdateFailed(f"Failed to fetch Phnix device data: {err}") from err
