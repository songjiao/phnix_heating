"""Binary Sensor platform for Phnix Heating integration."""
import logging
from typing import Any, Optional

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .phnix_api import PhnixAPI

_LOGGER = logging.getLogger(__name__)

# 简化的二进制传感器定义
BINARY_SENSORS = [
    {
        "key": "power_status",
        "name": "开关机状态",
        "address": "2011",
        "device_class": BinarySensorDeviceClass.POWER,
    },
    {
        "key": "mode_status",
        "name": "运行模式",
        "address": "2012",
        "device_class": BinarySensorDeviceClass.RUNNING,
    },
]

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Phnix Heating binary sensor platform."""
    api = hass.data[DOMAIN][config_entry.entry_id]
    
    entities = []
    for sensor_config in BINARY_SENSORS:
        entities.append(PhnixBinarySensor(api, config_entry, sensor_config))
    
    async_add_entities(entities, True)

class PhnixBinarySensor(BinarySensorEntity):
    """Representation of a Phnix Heating binary sensor."""
    
    _attr_has_entity_name = True
    
    def __init__(self, api: PhnixAPI, config_entry: ConfigEntry, sensor_config: dict):
        """Initialize the binary sensor."""
        self.api = api
        self.config_entry = config_entry
        self.sensor_config = sensor_config
        
        # 设置实体属性
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_config['key']}"
        self._attr_name = sensor_config["name"]
        self._attr_device_class = sensor_config["device_class"]
        
        # 状态属性
        self._attr_is_on = False
        self._attr_available = False
    
    async def async_update(self) -> None:
        """Update the binary sensor state."""
        try:
            # 获取设备状态
            status_data = await self.api.get_device_status()
            
            # 查找对应的数据
            address = self.sensor_config["address"]
            
            for item in status_data:
                if item["address"] == address:
                    value = item.get("dataValue")
                    self._attr_is_on = value == "1" if value is not None else False
                    break
            else:
                self._attr_is_on = False
            
            self._attr_available = True
            
        except Exception as e:
            _LOGGER.error("Failed to update binary sensor %s: %s", self._attr_name, e)
            self._attr_available = False 