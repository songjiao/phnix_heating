"""Sensor platform for Phnix Heating integration."""
import logging
from typing import Any

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
    UnitOfVolumeFlowRate,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import PhnixDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

# 传感器定义
SENSORS = [
    # 温度传感器
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
    {
        "key": "coil_temp",
        "name": "盘管温度",
        "address": "2049",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "suction_temp",
        "name": "回气温度",
        "address": "2051",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "exhaust_temp",
        "name": "排气温度",
        "address": "2053",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "frost_temp",
        "name": "防冻温度",
        "address": "2055",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "hot_water_temp",
        "name": "热水温度",
        "address": "2056",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "evi_inlet_temp",
        "name": "增焓进温度",
        "address": "2063",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "evi_outlet_temp",
        "name": "增焓出温度",
        "address": "2064",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    
    # 压力传感器
    {
        "key": "suction_pressure",
        "name": "回气压力",
        "address": "2070",
        "unit": UnitOfPressure.BAR,
        "device_class": SensorDeviceClass.PRESSURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "exhaust_pressure",
        "name": "排气压力",
        "address": "2071",
        "unit": UnitOfPressure.BAR,
        "device_class": SensorDeviceClass.PRESSURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    
    # 流量传感器
    {
        "key": "water_flow",
        "name": "水流量",
        "address": "2057",
        "unit": UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    
    # 电气参数传感器
    {
        "key": "ac_voltage",
        "name": "AC输入电压",
        "address": "2038",
        "unit": UnitOfElectricPotential.VOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "ac_current",
        "name": "AC输入电流",
        "address": "2039",
        "unit": UnitOfElectricCurrent.AMPERE,
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "comp_current",
        "name": "压缩机相电流",
        "address": "2040",
        "unit": UnitOfElectricCurrent.AMPERE,
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "dc_bus_voltage",
        "name": "DC母线电压",
        "address": "2041",
        "unit": UnitOfElectricPotential.VOLT,
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "ipm_temp",
        "name": "IPM温度",
        "address": "2042",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "power_input",
        "name": "电表输入功率",
        "address": "2031",
        "unit": UnitOfPower.WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "heat_pump_capacity",
        "name": "热泵能力",
        "address": "2032",
        "unit": UnitOfPower.KILO_WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "cop",
        "name": "COP",
        "address": "2033",
        "unit": None,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    
    # 运行参数传感器
    {
        "key": "comp_freq",
        "name": "压缩机频率",
        "address": "2025",
        "unit": UnitOfFrequency.HERTZ,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "fan1_speed",
        "name": "风机1转速",
        "address": "2029",
        "unit": "rpm",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "fan2_speed",
        "name": "风机2转速",
        "address": "2030",
        "unit": "rpm",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "eev_opening",
        "name": "电子膨胀阀开度",
        "address": "2020",
        "unit": None,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "evi_eev_opening",
        "name": "增焓电子膨胀阀开度",
        "address": "2021",
        "unit": None,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "comp_runtime",
        "name": "压缩机运行时间",
        "address": "2043",
        "unit": "h",
        "device_class": SensorDeviceClass.DURATION,
        "state_class": SensorStateClass.TOTAL_INCREASING,
    },
    {
        "key": "electricity",
        "name": "电表电量",
        "address": "2035",
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
    },
    
    # 通信状态传感器
    {
        "key": "dtu_signal",
        "name": "DTU信号强度",
        "address": "2037",
        "unit": None,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "dtu_online",
        "name": "DTU在线标志",
        "address": "2130",
        "unit": None,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "multi_unit_comm",
        "name": "多机组通信状态",
        "address": "2059",
        "unit": None,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
    },
]

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Phnix Heating sensor platform."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator: PhnixDataUpdateCoordinator = data["coordinator"]

    entities = []
    for sensor_config in SENSORS:
        entities.append(PhnixSensor(coordinator, config_entry, sensor_config))

    async_add_entities(entities)

class PhnixSensor(CoordinatorEntity[PhnixDataUpdateCoordinator], SensorEntity):
    """Representation of a Phnix Heating sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: PhnixDataUpdateCoordinator,
        config_entry: ConfigEntry,
        sensor_config: dict,
    ):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.sensor_config = sensor_config
        self._address = sensor_config["address"]

        # Set entity attributes
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_config['key']}"
        self._attr_name = sensor_config["name"]
        self._attr_native_unit_of_measurement = sensor_config["unit"]
        self._attr_device_class = sensor_config["device_class"]
        self._attr_state_class = sensor_config["state_class"]

    @property
    def native_value(self) -> Any:
        """Return the sensor value from coordinator data."""
        if not self.coordinator.data:
            return None

        by_address = self.coordinator.data.get("by_address", {})
        item = by_address.get(self._address)

        if not item:
            return None

        value = item.get("dataValue")
        if value is None:
            return None

        try:
            # Try to convert to numeric value
            if "." in str(value):
                return float(value)
            return int(value)
        except (ValueError, TypeError):
            return value 