"""Sensor platform for Phnix Heating integration."""
import logging
from typing import Any, Optional

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfTemperature,
    UnitOfPressure,
    UnitOfPower,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfSpeed,
    UnitOfVolumeFlowRate,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .phnix_api import PhnixAPI

_LOGGER = logging.getLogger(__name__)

# 简化的传感器定义
SENSORS = [
    {
        "key": "inlet_water_temp",
        "name": "进水温度",
        "address": "2045",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "outlet_water_temp",
        "name": "出水温度",
        "address": "2046",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "indoor_temp",
        "name": "室内温度",
        "address": "2047",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "ambient_temp",
        "name": "环境温度",
        "address": "2048",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
]

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Phnix Heating sensor platform."""
    api = hass.data[DOMAIN][config_entry.entry_id]
    
    entities = []
    for sensor_config in SENSORS:
        entities.append(PhnixSensor(api, config_entry, sensor_config))
    
    async_add_entities(entities, True)

class PhnixSensor(SensorEntity):
    """Representation of a Phnix Heating sensor."""
    
    _attr_has_entity_name = True
    
    def __init__(self, api: PhnixAPI, config_entry: ConfigEntry, sensor_config: dict):
        """Initialize the sensor."""
        self.api = api
        self.config_entry = config_entry
        self.sensor_config = sensor_config
        
        # 设置实体属性
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_config['key']}"
        self._attr_name = sensor_config["name"]
        self._attr_native_unit_of_measurement = sensor_config["unit"]
        self._attr_device_class = sensor_config["device_class"]
        self._attr_state_class = sensor_config["state_class"]
        
        # 状态属性
        self._attr_native_value = None
        self._attr_available = False
    
    async def async_update(self) -> None:
        """Update the sensor state."""
        try:
            # 获取设备状态
            status_data = await self.api.get_device_status()
            
            # 查找对应的数据
            address = self.sensor_config["address"]
            for item in status_data:
                if item["address"] == address:
                    value = item.get("dataValue")
                    if value is not None:
                        try:
                            # 尝试转换为数值
                            if "." in value:
                                self._attr_native_value = float(value)
                            else:
                                self._attr_native_value = int(value)
                        except (ValueError, TypeError):
                            self._attr_native_value = value
                    else:
                        self._attr_native_value = None
                    break
            else:
                self._attr_native_value = None
            
            self._attr_available = True
            
        except Exception as e:
            _LOGGER.error("Failed to update sensor %s: %s", self._attr_name, e)
            self._attr_available = False 