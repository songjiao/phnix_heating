"""Climate platform for Phnix Heating integration."""
import logging
from typing import Any, Optional

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_TEMPERATURE,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, MODE_COOL, MODE_HEAT, POWER_OFF, POWER_ON

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Phnix Heating climate platform."""
    api = hass.data[DOMAIN][config_entry.entry_id]
    
    async_add_entities([PhnixClimate(api, config_entry)], True)

class PhnixClimate(ClimateEntity):
    """Representation of a Phnix Heating climate entity."""
    
    _attr_has_entity_name = True
    _attr_name = "地暖主机"
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE |
        ClimateEntityFeature.TURN_OFF |
        ClimateEntityFeature.TURN_ON
    )
    _attr_hvac_modes = [HVACMode.COOL, HVACMode.HEAT, HVACMode.OFF]
    _attr_min_temp = 5.0
    _attr_max_temp = 60.0
    
    def __init__(self, api, config_entry: ConfigEntry):
        """Initialize the climate entity."""
        self.api = api
        self.config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_climate"
        
        # 状态属性
        self._attr_hvac_mode = HVACMode.OFF
        self._attr_target_temperature = None
        self._attr_current_temperature = None
        self._attr_available = False
    
    async def async_update(self) -> None:
        """Update the climate state."""
        try:
            # 获取设备状态
            status_data = await self.api.get_device_status()
            
            # 解析状态数据
            self._parse_status_data(status_data)
            
            self._attr_available = True
            
        except Exception as e:
            error_msg = str(e)
            # 如果是登录相关错误，记录为警告而不是错误，因为会自动重试
            if "请重新登录" in error_msg or "登录" in error_msg:
                _LOGGER.warning("Climate 更新时遇到登录问题，将自动重试: %s", error_msg)
            else:
                _LOGGER.error("Failed to update climate state: %s", e)
            self._attr_available = False
    
    def _parse_status_data(self, status_data: list) -> None:
        """Parse status data to update climate attributes."""
        power_status = None
        mode_status = None
        target_temp = None
        current_temp = None
        
        for item in status_data:
            address = item.get("address")
            data_value = item.get("dataValue")
            
            if address == "2011":  # 开关机状态
                power_status = data_value
            elif address == "2012":  # 运行模式
                mode_status = data_value
            elif address == "2047":  # 室内温度
                try:
                    current_temp = float(data_value) if data_value else None
                except (ValueError, TypeError):
                    pass
            elif address == "1158" and mode_status == MODE_COOL:  # 制冷温度设定
                try:
                    target_temp = float(data_value) if data_value else None
                except (ValueError, TypeError):
                    pass
            elif address == "1159" and mode_status == MODE_HEAT:  # 制热温度设定
                try:
                    target_temp = float(data_value) if data_value else None
                except (ValueError, TypeError):
                    pass
        
        # 更新HVAC模式
        if power_status == POWER_OFF:
            self._attr_hvac_mode = HVACMode.OFF
        elif mode_status == MODE_COOL:
            self._attr_hvac_mode = HVACMode.COOL
        elif mode_status == MODE_HEAT:
            self._attr_hvac_mode = HVACMode.HEAT
        else:
            self._attr_hvac_mode = HVACMode.OFF
        
        # 更新温度
        self._attr_current_temperature = current_temp
        self._attr_target_temperature = target_temp
    
    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        try:
            if hvac_mode == HVACMode.OFF:
                await self.api.set_power(False)
            else:
                # 先开机
                await self.api.set_power(True)
                
                # 设置模式
                if hvac_mode == HVACMode.COOL:
                    await self.api.set_mode("cool")
                elif hvac_mode == HVACMode.HEAT:
                    await self.api.set_mode("heat")
            
            # 立即更新状态
            await self.async_update()
            
        except Exception as e:
            _LOGGER.error("Failed to set HVAC mode: %s", e)
            raise
    
    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        try:
            temperature = kwargs.get(ATTR_TEMPERATURE)
            if temperature is None:
                return
            
            # 根据当前模式设置温度
            if self._attr_hvac_mode == HVACMode.COOL:
                await self.api.set_temperature(temperature, "cool")
            elif self._attr_hvac_mode == HVACMode.HEAT:
                await self.api.set_temperature(temperature, "heat")
            
            # 立即更新状态
            await self.async_update()
            
        except Exception as e:
            _LOGGER.error("Failed to set temperature: %s", e)
            raise
    
    async def async_turn_on(self) -> None:
        """Turn the entity on."""
        try:
            await self.api.set_power(True)
            await self.async_update()
        except Exception as e:
            _LOGGER.error("Failed to turn on: %s", e)
            raise
    
    async def async_turn_off(self) -> None:
        """Turn the entity off."""
        try:
            await self.api.set_power(False)
            await self.async_update()
        except Exception as e:
            _LOGGER.error("Failed to turn off: %s", e)
            raise 