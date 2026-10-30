import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval

from .history_manager import SYNC_TICK, HistoryManager
from .websocket_api import async_register_websocket

from .const import (
    CONF_TEAM_SLOT,
    DOMAIN,
)

from .coordinator import KNBSBCoordinator


_LOGGER = logging.getLogger(__name__)

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

    manager = hass.data.setdefault(DOMAIN, {}).get("history")

    if manager is None:
        manager = HistoryManager(hass)
        await manager.async_setup()
        hass.data[DOMAIN]["history"] = manager
        async_register_websocket(hass)

    async def _sync_history(force: bool = False) -> None:
        try:
            await manager.async_sync_team(
                coordinator.api,
                force=force,
            )
        except Exception as err:  # noqa: BLE001
            _LOGGER.warning(
                "KNBSB history sync failed for pool %s: %s",
                coordinator.pool_id,
                err,
            )

    async def _tick(_now) -> None:
        await _sync_history()

    entry.async_on_unload(
        async_track_time_interval(hass, _tick, SYNC_TICK)
    )

    # Always sync once after (re)start.
    entry.async_create_background_task(
        hass,
        _sync_history(force=True),
        "knbsb_history_initial_sync",
    )

    def _apply_stored_names() -> None:
        """Fill team names from history when no upcoming matches exist."""

        if coordinator.team_name:
            return

        team = manager.store.find_team_by_guid(coordinator.team_guid)

        if not team:
            return

        coordinator.club_name = team["club_name"]
        coordinator.team_name = team["team_code"]
        coordinator.team_display_name = (
            f"{team['club_name']} - {team['team_code']}"
        )

        hass.config_entries.async_update_entry(
            entry,
            title=coordinator.team_display_name,
        )

    if not coordinator.team_name:
        await _sync_history(force=True)
        _apply_stored_names()

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