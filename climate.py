"""Climate platform for Phnix Heating integration."""
import logging
from typing import Any, Optional

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
    HVACAction,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_TEMPERATURE,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    DOMAIN, MODE_COOL, MODE_HEAT, POWER_ON, POWER_OFF,
    COOL_TEMP_MIN, COOL_TEMP_MAX, HEAT_TEMP_MIN, HEAT_TEMP_MAX
)
from .phnix_api import PhnixAPI

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
    """Representation of a Phnix Heating climate device."""
    
    _attr_has_entity_name = True
    _attr_name = "Phnix地暖主机"
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE |
        ClimateEntityFeature.TURN_ON |
        ClimateEntityFeature.TURN_OFF
    )
    
    def __init__(self, api: PhnixAPI, config_entry: ConfigEntry):
        """Initialize the climate device."""
        self.api = api
        self.config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_climate"
        
        # 状态属性
        self._attr_hvac_mode = HVACMode.OFF
        self._attr_hvac_action = HVACAction.OFF
        self._attr_target_temperature = None
        self._attr_current_temperature = None
        self._attr_available = False
        
        # 温度范围
        self._attr_min_temp = COOL_TEMP_MIN
        self._attr_max_temp = HEAT_TEMP_MAX
        
        # 支持的模式
        self._attr_hvac_modes = [HVACMode.OFF, HVACMode.COOL, HVACMode.HEAT]
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._attr_available
    
    async def async_update(self) -> None:
        """Update the climate state."""
        try:
            # 获取设备状态
            status_data = await self.api.get_device_status()
            
            # 解析状态数据
            self._parse_status_data(status_data)
            
            self._attr_available = True
            
        except Exception as e:
            _LOGGER.error("Failed to update climate state: %s", e)
            self._attr_available = False
    
    def _parse_status_data(self, status_data: list) -> None:
        """Parse status data and update entity state."""
        # 创建地址到数据的映射
        data_map = {item["address"]: item for item in status_data}
        
        # 解析开关机状态
        power_status = data_map.get("2011", {})
        power_value = power_status.get("dataValue", "0")
        is_powered = power_value == "1"
        
        # 解析运行模式
        mode_status = data_map.get("2012", {})
        mode_value = mode_status.get("dataValue", "0")
        
        # 解析温度数据
        indoor_temp = data_map.get("2047", {})
        current_temp = indoor_temp.get("dataValue")
        
        # 解析目标温度
        target_temp = None
        if mode_value == MODE_COOL:
            cool_config = data_map.get("1158", {})
            target_temp = cool_config.get("dataValue")
        elif mode_value == MODE_HEAT:
            heat_config = data_map.get("1159", {})
            target_temp = heat_config.get("dataValue")
        
        # 更新实体状态
        if not is_powered:
            self._attr_hvac_mode = HVACMode.OFF
            self._attr_hvac_action = HVACAction.OFF
        else:
            if mode_value == MODE_COOL:
                self._attr_hvac_mode = HVACMode.COOL
                self._attr_hvac_action = HVACAction.COOLING
            elif mode_value == MODE_HEAT:
                self._attr_hvac_mode = HVACMode.HEAT
                self._attr_hvac_action = HVACAction.HEATING
            else:
                self._attr_hvac_mode = HVACMode.OFF
                self._attr_hvac_action = HVACAction.OFF
        
        # 更新温度
        if current_temp is not None:
            try:
                self._attr_current_temperature = float(current_temp)
            except (ValueError, TypeError):
                self._attr_current_temperature = None
        
        if target_temp is not None:
            try:
                self._attr_target_temperature = float(target_temp)
            except (ValueError, TypeError):
                self._attr_target_temperature = None
    
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
                    await self.api.set_mode(MODE_COOL)
                elif hvac_mode == HVACMode.HEAT:
                    await self.api.set_mode(MODE_HEAT)
            
            # 立即更新状态
            await self.async_update()
            
        except Exception as e:
            _LOGGER.error("Failed to set HVAC mode: %s", e)
            raise
    
    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        target_temp = kwargs.get(ATTR_TEMPERATURE)
        if target_temp is None:
            return
        
        try:
            # 根据当前模式设置温度
            is_cooling = self._attr_hvac_mode == HVACMode.COOL
            
            # 验证温度范围
            if is_cooling:
                if not COOL_TEMP_MIN <= target_temp <= COOL_TEMP_MAX:
                    raise ValueError(f"Cooling temperature must be between {COOL_TEMP_MIN} and {COOL_TEMP_MAX}")
            else:
                if not HEAT_TEMP_MIN <= target_temp <= HEAT_TEMP_MAX:
                    raise ValueError(f"Heating temperature must be between {HEAT_TEMP_MIN} and {HEAT_TEMP_MAX}")
            
            await self.api.set_temperature(target_temp, is_cooling)
            
            # 立即更新状态
            await self.async_update()
            
        except Exception as e:
            _LOGGER.error("Failed to set temperature: %s", e)
            raise
    
    async def async_turn_on(self) -> None:
        """Turn the device on."""
        await self.async_set_hvac_mode(HVACMode.HEAT)
    
    async def async_turn_off(self) -> None:
        """Turn the device off."""
        await self.async_set_hvac_mode(HVACMode.OFF) 