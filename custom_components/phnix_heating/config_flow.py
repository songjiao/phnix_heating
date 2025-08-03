"""Config flow for Phnix Heating integration."""
import logging
import voluptuous as vol
from typing import Any, Dict, Optional

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.const import CONF_NAME

from .const import DOMAIN
from .phnix_api import PhnixAPI

_LOGGER = logging.getLogger(__name__)

class PhnixHeatingConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Phnix Heating."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                # 创建API客户端进行登录测试
                api = PhnixAPI(
                    username=user_input["username"],
                    password=user_input["password"],
                    device_code=user_input["device_code"]
                )
                
                # 测试登录
                await api.login()
                
                # 测试设备连接
                await api.get_device_status()
                
                # 创建配置项
                config_data = {
                    "username": user_input["username"],
                    "password": user_input["password"],
                    "device_code": user_input["device_code"],
                    "name": user_input.get("name", "地暖主机")
                }
                
                return self.async_create_entry(
                    title=config_data["name"],
                    data=config_data
                )
                
            except Exception as ex:
                _LOGGER.error("配置验证失败: %s", ex)
                errors["base"] = "cannot_connect"

        # 显示配置表单
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("username"): str,
                vol.Required("password"): str,
                vol.Required("device_code"): str,
                vol.Optional("name", default="地暖主机"): str,
            }),
            errors=errors,
        )

    async def async_step_import(self, import_info: Dict[str, Any]) -> FlowResult:
        """Handle import from configuration.yaml."""
        return await self.async_step_user(import_info) 