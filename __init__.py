from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .coordinator import KNBSBCoordinator


PLATFORMS = [
    "sensor",
    "calendar",
]


async def async_setup(
    hass: HomeAssistant,
    config: dict,
) -> bool:
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:

    coordinator = KNBSBCoordinator(
        hass,
        entry,
    )

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:

    return await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )