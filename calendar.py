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
        super().__init__(coordinator)

        self._attr_name = "KNBSB Team"
        self._attr_unique_id = "knbsb_calendar"


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

    coordinator = entry.runtime_data

    async_add_entities(
        [
            KNBSBCalendarEntity(
                coordinator
            )
        ]
    )