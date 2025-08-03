"""Config flow for Phnix Heating integration."""
import logging
import voluptuous as vol
from typing import Any, Dict, Optional

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.const import CONF_NAME

from .const import (
    DOMAIN, CONF_DEVICE_CODE, CONF_PROTOCOL_ID, CONF_TOKEN, 
    CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DEFAULT_PROTOCOL_ID
)
from .phnix_api import PhnixAPI, PhnixAPIError

_LOGGER = logging.getLogger(__name__)

class PhnixHeatingConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Phnix Heating."""
    
    VERSION = 1
    
    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            try:
                # 验证连接
                api = PhnixAPI(
                    token=user_input[CONF_TOKEN],
                    device_code=user_input[CONF_DEVICE_CODE],
                    protocol_id=user_input.get(CONF_PROTOCOL_ID, DEFAULT_PROTOCOL_ID)
                )
                
                # 测试连接
                await api.get_device_status()
                await api.close()
                
                # 创建配置条目
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input
                )
                
            except PhnixAPIError as e:
                errors["base"] = "cannot_connect"
                _LOGGER.error("Connection test failed: %s", e)
            except Exception as e:
                errors["base"] = "unknown"
                _LOGGER.error("Unexpected error: %s", e)
        
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME): str,
                vol.Required(CONF_DEVICE_CODE): str,
                vol.Required(CONF_TOKEN): str,
                vol.Optional(CONF_PROTOCOL_ID, default=DEFAULT_PROTOCOL_ID): str,
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
            }),
            errors=errors,
        )
    
    async def async_step_import(self, import_info: Dict[str, Any]) -> FlowResult:
        """Handle import from configuration.yaml."""
        return await self.async_step_user(import_info) 