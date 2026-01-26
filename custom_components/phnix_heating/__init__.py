"""The Phnix Heating integration."""
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, PLATFORMS
from .coordinator import PhnixDataUpdateCoordinator
from .phnix_api import PhnixAPI, PhnixAPIError

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Phnix Heating from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Get configuration data
    username = entry.data["username"]
    password = entry.data["password"]
    device_code = entry.data["device_code"]

    # Create API client
    api = PhnixAPI(username=username, password=password, device_code=device_code)

    try:
        # Login to establish session
        await api.login()

        # Create coordinator for centralized data fetching
        coordinator = PhnixDataUpdateCoordinator(hass, api, device_code)

        # Fetch initial data (will raise ConfigEntryNotReady on failure)
        await coordinator.async_config_entry_first_refresh()

        # Store API and coordinator for platforms to access
        hass.data[DOMAIN][entry.entry_id] = {
            "api": api,
            "coordinator": coordinator,
        }

        # Set up platforms
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

        return True

    except PhnixAPIError as ex:
        _LOGGER.error("无法连接到Phnix设备: %s", ex)
        raise ConfigEntryNotReady from ex
    except Exception as ex:
        _LOGGER.error("设置Phnix Heating时发生未知错误: %s", ex)
        return False

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        # Close API connection
        data = hass.data[DOMAIN].pop(entry.entry_id)
        await data["api"].close()

    return unload_ok 