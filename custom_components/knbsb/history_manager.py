from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta

from homeassistant.core import HomeAssistant

from .history_models import normalize_match
from .history_store import HistoryStore

_LOGGER = logging.getLogger(__name__)

SYNC_TICK = timedelta(hours=1)
SYNC_INTERVAL_ACTIVE = timedelta(hours=1)
SYNC_INTERVAL_IDLE = timedelta(days=1)
ACTIVE_WINDOW = timedelta(days=1)


class HistoryManager:
    """Fetches all matches of a team's pool and stores them centrally."""

    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass
        self.store = HistoryStore(hass)

    async def async_setup(self) -> None:
        await self.store.async_load()

    def _has_active_match(self, pool_id: int, team_guid: str) -> bool:
        pool = self.store.get_pool(pool_id)

        if not pool:
            return False

        now = datetime.now()

        for match in pool["matches"].values():
            if team_guid not in (
                match["home_team_guid"],
                match["away_team_guid"],
            ):
                continue

            try:
                start = datetime.strptime(
                    f"{match['date']} {match['time'] or '00:00'}",
                    "%Y-%m-%d %H:%M",
                )
            except ValueError:
                continue

            if abs(start - now) <= ACTIVE_WINDOW:
                return True

        return False

    def is_due(self, api) -> bool:
        last = self.store.get_last_sync(api.team_guid)

        if not last:
            return True

        age = datetime.now(UTC) - datetime.fromisoformat(last)
        interval = (
            SYNC_INTERVAL_ACTIVE
            if self._has_active_match(api.pool_id, api.team_guid)
            else SYNC_INTERVAL_IDLE
        )

        return age >= interval

    async def async_sync_team(self, api, force: bool = False) -> bool:
        """Sync one team's pool. Returns True when a fetch happened."""

        if not force and not self.is_due(api):
            return False

        items = await api.get_pool_matches()
        now = datetime.now(UTC).isoformat()

        matches = [normalize_match(item) for item in items]

        for item in items:
            if item.get("homeTeamGuid") == api.team_guid:
                club = (item.get("homeOrganisation") or {}).get("name")
                code = item.get("homeTeamName")
            elif item.get("awayTeamGuid") == api.team_guid:
                club = (item.get("awayOrganisation") or {}).get("name")
                code = item.get("awayTeamName")
            else:
                continue

            if club and code:
                self.store.register_team(
                    club, code, api.team_guid, api.pool_id
                )
                break

        self.store.update_pool(api.pool_id, matches, now)
        self.store.set_last_sync(api.team_guid, now)
        await self.store.async_save()

        _LOGGER.debug(
            "KNBSB history synced: pool %s, %s matches",
            api.pool_id,
            len(matches),
        )

        return True
