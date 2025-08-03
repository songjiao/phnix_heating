"""The Phnix Heating integration."""
import logging
from typing import Any, Dict

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .phnix_api import PhnixAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.CLIMATE, Platform.SENSOR, Platform.BINARY_SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Phnix Heating from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # 创建API客户端
    api = PhnixAPI(
        token=entry.data["token"],
        device_code=entry.data["device_code"],
        protocol_id=entry.data.get("protocol_id", "1679324789907087360")
    )
    
    # 测试连接
    try:
        await api.get_device_status()
    except Exception as e:
        await api.close()
        raise ConfigEntryNotReady(f"Failed to connect to device: {e}") from e
    
    # 存储API客户端
    hass.data[DOMAIN][entry.entry_id] = api
    
    # 设置平台
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        api = hass.data[DOMAIN].pop(entry.entry_id)
        await api.close()
    
    return unload_ok 