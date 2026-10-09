from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    CONF_TEAM_SLOT,
    DOMAIN,
)

from .coordinator import KNBSBCoordinator


PLATFORMS = [
    "sensor",
    "calendar",
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up KNBSB from a config entry."""

    #
    # Bestaande single-team installaties
    # hebben nog geen team_slot.
    #
    # Ken automatisch het eerste vrije slot toe.
    #

    if CONF_TEAM_SLOT not in entry.data:

        used_slots = {
            existing_entry.data.get(
                CONF_TEAM_SLOT
            )
            for existing_entry
            in hass.config_entries.async_entries(
                DOMAIN
            )
            if (
                existing_entry.entry_id
                != entry.entry_id
                and existing_entry.data.get(
                    CONF_TEAM_SLOT
                )
                is not None
            )
        }

        team_slot = 1

        while team_slot in used_slots:
            team_slot += 1

        new_data = {
            **entry.data,
            CONF_TEAM_SLOT: team_slot,
        }

        hass.config_entries.async_update_entry(
            entry,
            data=new_data,
        )


    coordinator = KNBSBCoordinator(
        hass,
        entry,
    )

    await coordinator.async_config_entry_first_refresh()

    entry_title = (
        coordinator.team_display_name
        or coordinator.team_name
        or coordinator.club_name
        or f"KNBSB Team {coordinator.team_slot}"
    )

    if entry.title != entry_title:
        hass.config_entries.async_update_entry(
            entry,
            title=entry_title,
        )

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
    """Unload a KNBSB config entry."""

    return await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )