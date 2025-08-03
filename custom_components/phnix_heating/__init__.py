"""The Phnix Heating integration."""
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, PLATFORMS
from .phnix_api import PhnixAPI, PhnixAPIError

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Phnix Heating from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # 获取配置数据
    username = entry.data["username"]
    password = entry.data["password"]
    device_code = entry.data["device_code"]
    
    # 创建API客户端
    api = PhnixAPI(username=username, password=password, device_code=device_code)
    
    try:
        # 测试登录和连接
        await api.login()
        await api.get_device_status()
        
        # 存储API实例
        hass.data[DOMAIN][entry.entry_id] = api
        
        # 设置平台
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
        # 关闭API连接
        api = hass.data[DOMAIN].pop(entry.entry_id)
        await api.close()
    
    return unload_ok 