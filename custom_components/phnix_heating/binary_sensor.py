"""Binary Sensor platform for Phnix Heating integration."""
import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import PhnixDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

# 二进制传感器定义
BINARY_SENSORS = [
    # 设备状态
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
    {
        "key": "function_status",
        "name": "运行功能",
        "address": "2013",
        "device_class": BinarySensorDeviceClass.RUNNING,
    },
    
    # 输出状态 (address: 2019)
    {
        "key": "compressor_output",
        "name": "压缩机输出",
        "address": "2019",
        "num": "O01",
        "device_class": BinarySensorDeviceClass.RUNNING,
    },
    {
        "key": "secondary_pump_output",
        "name": "二次泵输出",
        "address": "2019",
        "num": "O02",
        "device_class": BinarySensorDeviceClass.RUNNING,
    },
    {
        "key": "high_fan_output",
        "name": "高风输出",
        "address": "2019",
        "num": "O03",
        "device_class": BinarySensorDeviceClass.RUNNING,
    },
    {
        "key": "low_fan_output",
        "name": "低风输出",
        "address": "2019",
        "num": "O04",
        "device_class": BinarySensorDeviceClass.RUNNING,
    },
    {
        "key": "four_way_valve_output",
        "name": "四通阀输出",
        "address": "2019",
        "num": "O05",
        "device_class": BinarySensorDeviceClass.RUNNING,
    },
    {
        "key": "hot_water_valve_output",
        "name": "热水三通阀输出",
        "address": "2019",
        "num": "O06",
        "device_class": BinarySensorDeviceClass.RUNNING,
    },
    {
        "key": "water_pump_output",
        "name": "水泵输出",
        "address": "2019",
        "num": "O07",
        "device_class": BinarySensorDeviceClass.RUNNING,
    },
    {
        "key": "electric_heat_output",
        "name": "电加热输出",
        "address": "2019",
        "num": "O08",
        "device_class": BinarySensorDeviceClass.HEAT,
    },
    {
        "key": "spray_valve_output",
        "name": "喷淋阀输出",
        "address": "2019",
        "num": "O09",
        "device_class": BinarySensorDeviceClass.RUNNING,
    },
    {
        "key": "frost_heat_output",
        "name": "防冻加热带输出",
        "address": "2019",
        "num": "O10",
        "device_class": BinarySensorDeviceClass.HEAT,
    },
    {
        "key": "crankcase_heat_output",
        "name": "曲轴加热带输出",
        "address": "2019",
        "num": "O11",
        "device_class": BinarySensorDeviceClass.HEAT,
    },
    {
        "key": "water_supply_output",
        "name": "补水阀输出",
        "address": "2019",
        "num": "bit11",
        "device_class": BinarySensorDeviceClass.RUNNING,
    },
    {
        "key": "alarm_output",
        "name": "报警输出",
        "address": "2019",
        "num": "O13",
        "device_class": BinarySensorDeviceClass.PROBLEM,
    },
    {
        "key": "cool_water_valve_output",
        "name": "制冷水阀输出",
        "address": "2019",
        "num": "bit13",
        "device_class": BinarySensorDeviceClass.RUNNING,
    },
    {
        "key": "heat_water_valve_output",
        "name": "制热水阀输出",
        "address": "2019",
        "num": "bit14",
        "device_class": BinarySensorDeviceClass.RUNNING,
    },
    
    # 安全开关状态 (address: 2034)
    {
        "key": "high_pressure_switch",
        "name": "高压开关",
        "address": "2034",
        "num": "S01",
        "device_class": BinarySensorDeviceClass.SAFETY,
    },
    {
        "key": "low_pressure_switch",
        "name": "低压开关",
        "address": "2034",
        "num": "S03",
        "device_class": BinarySensorDeviceClass.SAFETY,
    },
    {
        "key": "water_flow_switch",
        "name": "水流开关",
        "address": "2034",
        "num": "S04",
        "device_class": BinarySensorDeviceClass.SAFETY,
    },
    {
        "key": "dry_burn_switch",
        "name": "电加热干烧开关",
        "address": "2034",
        "num": "S05",
        "device_class": BinarySensorDeviceClass.SAFETY,
    },
    {
        "key": "mode_input_switch",
        "name": "模式输入",
        "address": "2034",
        "num": "S06",
        "device_class": BinarySensorDeviceClass.RUNNING,
    },
    {
        "key": "emergency_switch",
        "name": "应急开关",
        "address": "2034",
        "num": "S09",
        "device_class": BinarySensorDeviceClass.SAFETY,
    },
]

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Phnix Heating binary sensor platform."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator: PhnixDataUpdateCoordinator = data["coordinator"]

    entities = []
    for sensor_config in BINARY_SENSORS:
        entities.append(PhnixBinarySensor(coordinator, config_entry, sensor_config))

    async_add_entities(entities)


class PhnixBinarySensor(CoordinatorEntity[PhnixDataUpdateCoordinator], BinarySensorEntity):
    """Representation of a Phnix Heating binary sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: PhnixDataUpdateCoordinator,
        config_entry: ConfigEntry,
        sensor_config: dict,
    ):
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.sensor_config = sensor_config
        self._address = sensor_config["address"]
        self._num = sensor_config.get("num")

        # Set entity attributes
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_config['key']}"
        self._attr_name = sensor_config["name"]
        self._attr_device_class = sensor_config["device_class"]

    @property
    def is_on(self) -> bool:
        """Return True if the binary sensor is on."""
        if not self.coordinator.data:
            return False

        if self._num:
            # For multi-value addresses (2019, 2034), use (address, num) lookup
            by_address_num = self.coordinator.data.get("by_address_num", {})
            item = by_address_num.get((self._address, self._num))
        else:
            # For simple addresses, use address-only lookup
            by_address = self.coordinator.data.get("by_address", {})
            item = by_address.get(self._address)

        if not item:
            return False

        value = item.get("dataValue")
        return value == "1" if value is not None else False 