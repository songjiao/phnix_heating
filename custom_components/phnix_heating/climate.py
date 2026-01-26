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
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MODE_COOL, MODE_HEAT, POWER_OFF
from .coordinator import PhnixDataUpdateCoordinator
from .phnix_api import PhnixAPI

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Phnix Heating climate platform."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator: PhnixDataUpdateCoordinator = data["coordinator"]
    api: PhnixAPI = data["api"]

    async_add_entities([PhnixClimate(coordinator, api, config_entry)])


class PhnixClimate(CoordinatorEntity[PhnixDataUpdateCoordinator], ClimateEntity):
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

    def __init__(
        self,
        coordinator: PhnixDataUpdateCoordinator,
        api: PhnixAPI,
        config_entry: ConfigEntry,
    ):
        """Initialize the climate entity."""
        super().__init__(coordinator)
        self.api = api
        self.config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_climate"

    @property
    def hvac_mode(self) -> HVACMode:
        """Return current HVAC mode."""
        if not self.coordinator.data:
            return HVACMode.OFF

        by_address = self.coordinator.data.get("by_address", {})

        power_item = by_address.get("2011")
        mode_item = by_address.get("2012")

        power_status = power_item.get("dataValue") if power_item else None
        mode_status = mode_item.get("dataValue") if mode_item else None

        if power_status == POWER_OFF:
            return HVACMode.OFF
        elif mode_status == MODE_COOL:
            return HVACMode.COOL
        elif mode_status == MODE_HEAT:
            return HVACMode.HEAT
        return HVACMode.OFF

    @property
    def current_temperature(self) -> Optional[float]:
        """Return current temperature."""
        if not self.coordinator.data:
            return None

        by_address = self.coordinator.data.get("by_address", {})
        item = by_address.get("2047")

        if not item:
            return None

        try:
            value = item.get("dataValue")
            return float(value) if value else None
        except (ValueError, TypeError):
            return None

    @property
    def target_temperature(self) -> Optional[float]:
        """Return target temperature based on current mode."""
        if not self.coordinator.data:
            return None

        by_address = self.coordinator.data.get("by_address", {})
        mode_item = by_address.get("2012")
        mode_status = mode_item.get("dataValue") if mode_item else None

        # Select address based on mode
        if mode_status == MODE_COOL:
            address = "1158"
        elif mode_status == MODE_HEAT:
            address = "1159"
        else:
            return None

        item = by_address.get(address)
        if not item:
            return None

        try:
            value = item.get("dataValue")
            return float(value) if value else None
        except (ValueError, TypeError):
            return None

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        try:
            if hvac_mode == HVACMode.OFF:
                await self.api.set_power(False)
            else:
                # Turn on first
                await self.api.set_power(True)

                # Set mode
                if hvac_mode == HVACMode.COOL:
                    await self.api.set_mode("cool")
                elif hvac_mode == HVACMode.HEAT:
                    await self.api.set_mode("heat")

            # Request coordinator refresh to update all entities
            await self.coordinator.async_request_refresh()

        except Exception as e:
            _LOGGER.error("Failed to set HVAC mode: %s", e)
            raise

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        try:
            temperature = kwargs.get(ATTR_TEMPERATURE)
            if temperature is None:
                return

            # Set temperature based on current mode
            current_mode = self.hvac_mode
            if current_mode == HVACMode.COOL:
                await self.api.set_temperature(temperature, "cool")
            elif current_mode == HVACMode.HEAT:
                await self.api.set_temperature(temperature, "heat")

            # Request coordinator refresh to update all entities
            await self.coordinator.async_request_refresh()

        except Exception as e:
            _LOGGER.error("Failed to set temperature: %s", e)
            raise

    async def async_turn_on(self) -> None:
        """Turn the entity on."""
        try:
            await self.api.set_power(True)
            await self.coordinator.async_request_refresh()
        except Exception as e:
            _LOGGER.error("Failed to turn on: %s", e)
            raise

    async def async_turn_off(self) -> None:
        """Turn the entity off."""
        try:
            await self.api.set_power(False)
            await self.coordinator.async_request_refresh()
        except Exception as e:
            _LOGGER.error("Failed to turn off: %s", e)
            raise 