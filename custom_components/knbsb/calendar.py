from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from homeassistant.components.calendar import (
    CalendarEntity,
    CalendarEvent,
)
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)


class KNBSBCalendarEntity(
    CoordinatorEntity,
    CalendarEntity,
):

    def __init__(
        self,
        coordinator,
    ):
        super().__init__(
            coordinator
        )

        team_display_name = (
            coordinator.team_display_name
            or coordinator.team_name
            or coordinator.club_name
            or f"KNBSB Team {coordinator.team_slot}"
        )

        self._attr_name = (
            f"{team_display_name} - Kalender"
        )

        self._attr_unique_id = (
            f"knbsb_"
            f"{coordinator.team_guid}_"
            f"calendar"
        )


    def _build_datetime(
        self,
        match,
    ):
        """Build timezone-aware KNBSB match datetime."""

        dt = datetime.strptime(
            f"{match.date} {match.time}",
            "%Y-%m-%d %H:%M",
        )

        return dt.replace(
            tzinfo=ZoneInfo(
                "Europe/Amsterdam"
            )
        )


    @property
    def event(self):
        """Return the next KNBSB match."""

        match = self.coordinator.data.get(
            "next_match"
        )

        if not match:
            return None

        start = self._build_datetime(
            match
        )

        end = start + timedelta(
            hours=2
        )

        return CalendarEvent(
            summary=(
                f"{match.opponent} "
                f"({match.home_away})"
            ),
            start=start,
            end=end,
            location=match.location,
            description=match.competition,
        )


    async def async_get_events(
        self,
        hass,
        start_date,
        end_date,
    ):
        """Return KNBSB matches for the requested period."""

        events = []

        for match in self.coordinator.data.get(
            "matches",
            [],
        ):
            start = self._build_datetime(
                match
            )

            end = start + timedelta(
                hours=2
            )

            #
            # Alleen wedstrijden binnen het
            # door HA gevraagde tijdvak.
            #

            if (
                start >= end_date
                or end <= start_date
            ):
                continue

            events.append(
                CalendarEvent(
                    summary=(
                        f"{match.opponent} "
                        f"({match.home_away})"
                    ),
                    start=start,
                    end=end,
                    location=match.location,
                    description=match.competition,
                )
            )

        return events


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    """Set up the KNBSB calendar for this team."""

    coordinator = entry.runtime_data

    async_add_entities(
        [
            KNBSBCalendarEntity(
                coordinator
            )
        ]
    )