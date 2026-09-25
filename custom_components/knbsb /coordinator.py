import logging

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from homeassistant.helpers.aiohttp_client import (
    async_get_clientsession,
)

from homeassistant.helpers.storage import Store

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from .api import (
    FoysApi,
    parse_team_url,
)

from .const import (
    CONF_ORS_API_KEY,
    CONF_TEAM_URL,
    CONF_AWAY_ARRIVAL_MINUTES,
    CONF_HOME_ARRIVAL_MINUTES,
    PARKING_BUFFER_MINUTES,
    TRAVEL_BUFFER_PERCENT,
    UPDATE_INTERVAL,
)


_LOGGER = logging.getLogger(__name__)


STORAGE_VERSION = 1
STORAGE_KEY = "knbsb.travel_cache"


class KNBSBCoordinator(DataUpdateCoordinator):

    def __init__(
        self,
        hass,
        entry,
    ):
        self.config_entry = entry

        self.ors_api_key = entry.data.get(
            CONF_ORS_API_KEY,
            "",
        )

        parsed = parse_team_url(
            entry.data[CONF_TEAM_URL]
        )

        _LOGGER.warning(
            "KNBSB URL PARSED | org=%s team=%s pool=%s",
            parsed["organisation_id"],
            parsed["team_guid"],
            parsed["pool_id"],
        )

        session = async_get_clientsession(
            hass
        )

        self.api = FoysApi(
            session=session,
            organisation_id=parsed["organisation_id"],
            team_guid=parsed["team_guid"],
            pool_id=parsed["pool_id"],
            ors_api_key=self.ors_api_key,
        )

        #
        # Travel cache in RAM
        #

        self._travel_cache = {}

        self._travel_cache_loaded = False


        #
        # Persistente Home Assistant storage.
        #
        # Iedere config entry krijgt zijn eigen cache.
        #

        self._travel_store = Store(
            hass,
            STORAGE_VERSION,
            f"{STORAGE_KEY}.{entry.entry_id}",
        )


        super().__init__(
            hass,
            _LOGGER,
            name="KNBSB",
            update_interval=UPDATE_INTERVAL,
        )


    #
    # ---------------------------------------------------------
    # MATCH DATETIME
    # ---------------------------------------------------------
    #

    def _get_match_datetime(
        self,
        match,
    ):
        """Maak timezone-aware datetime van wedstrijd."""

        timezone = ZoneInfo(
            self.hass.config.time_zone
        )

        match_dt = datetime.strptime(
            f"{match.date} {match.time}",
            "%Y-%m-%d %H:%M",
        )

        return match_dt.replace(
            tzinfo=timezone
        )


    #
    # ---------------------------------------------------------
    # PLANNING
    # ---------------------------------------------------------
    #

    def _calculate_planning(
        self,
        match,
        drive_time,
    ):
        """Bereken aankomst- en vertrektijd."""

        match_dt = self._get_match_datetime(
            match
        )

        travel_buffer = round(
            drive_time
            * TRAVEL_BUFFER_PERCENT
            / 100
        )


        if match.home_away == "Uit":

            arrival_buffer = (
                self.config_entry.data.get(
                    CONF_AWAY_ARRIVAL_MINUTES,
                    30,
                )
            )

        else:

            arrival_buffer = (
                self.config_entry.data.get(
                    CONF_HOME_ARRIVAL_MINUTES,
                    15,
                )
            )


        arrival_time = (
            match_dt
            - timedelta(
                minutes=(
                    arrival_buffer
                    + PARKING_BUFFER_MINUTES
                )
            )
        )


        total_departure_buffer = (
            drive_time
            + travel_buffer
            + arrival_buffer
            + PARKING_BUFFER_MINUTES
        )


        departure_time = (
            match_dt
            - timedelta(
                minutes=total_departure_buffer
            )
        )


        return {
            "arrival_time":
                arrival_time,

            "departure_time":
                departure_time,

            "travel_buffer":
                travel_buffer,

            "arrival_buffer":
                arrival_buffer,
        }


    #
    # ---------------------------------------------------------
    # PERSISTENTE CACHE LADEN
    # ---------------------------------------------------------
    #

    async def _async_load_travel_cache(
        self,
    ):
        """Laad travel cache vanuit Home Assistant storage."""

        stored_data = (
            await self._travel_store.async_load()
        )


        if not stored_data:

            self._travel_cache = {}

            return


        cache = {}


        for match_id, item in stored_data.items():

            try:

                internal_match_id = int(
                    match_id
                )


                updated = item.get(
                    "updated"
                )

                if updated:

                    updated = (
                        datetime.fromisoformat(
                            updated
                        )
                    )


                arrival_time = item.get(
                    "arrival_time"
                )

                if arrival_time:

                    arrival_time = (
                        datetime.fromisoformat(
                            arrival_time
                        )
                    )


                departure_time = item.get(
                    "departure_time"
                )

                if departure_time:

                    departure_time = (
                        datetime.fromisoformat(
                            departure_time
                        )
                    )


                cache[
                    internal_match_id
                ] = {
                    "latitude":
                        item.get(
                            "latitude"
                        ),

                    "longitude":
                        item.get(
                            "longitude"
                        ),

                    "drive_distance":
                        item.get(
                            "drive_distance"
                        ),

                    "drive_time":
                        item.get(
                            "drive_time"
                        ),

                    "travel_buffer":
                        item.get(
                            "travel_buffer"
                        ),

                    "arrival_buffer":
                        item.get(
                            "arrival_buffer"
                        ),

                    "arrival_time":
                        arrival_time,

                    "departure_time":
                        departure_time,

                    "updated":
                        updated,
                }


            except (
                TypeError,
                ValueError,
                KeyError,
            ) as err:

                _LOGGER.warning(
                    "Invalid KNBSB travel cache entry "
                    "%s ignored: %s",
                    match_id,
                    err,
                )


        self._travel_cache = cache




    #
    # ---------------------------------------------------------
    # PERSISTENTE CACHE OPSLAAN
    # ---------------------------------------------------------
    #

    async def _async_save_travel_cache(
        self,
    ):
        """Sla travel cache op in Home Assistant storage."""

        stored_data = {}


        for match_id, item in (
            self._travel_cache.items()
        ):

            stored_data[
                str(match_id)
            ] = {
                "latitude":
                    item.get(
                        "latitude"
                    ),

                "longitude":
                    item.get(
                        "longitude"
                    ),

                "drive_distance":
                    item.get(
                        "drive_distance"
                    ),

                "drive_time":
                    item.get(
                        "drive_time"
                    ),

                "travel_buffer":
                    item.get(
                        "travel_buffer"
                    ),

                "arrival_buffer":
                    item.get(
                        "arrival_buffer"
                    ),

                "arrival_time":
                    (
                        item[
                            "arrival_time"
                        ].isoformat()
                        if item.get(
                            "arrival_time"
                        )
                        else None
                    ),

                "departure_time":
                    (
                        item[
                            "departure_time"
                        ].isoformat()
                        if item.get(
                            "departure_time"
                        )
                        else None
                    ),

                "updated":
                    (
                        item[
                            "updated"
                        ].isoformat()
                        if item.get(
                            "updated"
                        )
                        else None
                    ),
            }


        await self._travel_store.async_save(
            stored_data
        )


        _LOGGER.debug(
            "KNBSB travel cache opgeslagen: %s routes",
            len(
                stored_data
            ),
        )


    #
    # ---------------------------------------------------------
    # ROUTE PER WEDSTRIJD
    # ---------------------------------------------------------
    #

    async def _async_get_match_travel(
        self,
        match,
        home_lat,
        home_lon,
        force_refresh=False,
    ):
        """Haal of hergebruik reisinformatie voor wedstrijd."""

        cached = self._travel_cache.get(
            match.match_id
        )


        location_changed = False


        if cached:

            location_changed = (
                cached.get(
                    "latitude"
                )
                != match.latitude
                or
                cached.get(
                    "longitude"
                )
                != match.longitude
            )


        #
        # Bestaande cache gebruiken.
        #

        if (
            cached
            and not force_refresh
            and not location_changed
        ):

            return cached


        #
        # Nieuwe ORS route ophalen.
        #

        try:

            route = await self.api.get_drive_info(
                home_lat,
                home_lon,
                match.latitude,
                match.longitude,
            )

        except Exception as err:

            _LOGGER.error(
                "ORS lookup failed for match %s: %s",
                match.match_id,
                err,
            )

            #
            # Oude cache blijft beschikbaar
            # wanneer ORS tijdelijk faalt.
            #

            return cached


        drive_distance = route[
            "distance_km"
        ]

        drive_time = route[
            "duration_min"
        ]


        planning = self._calculate_planning(
            match,
            drive_time,
        )


        now = datetime.now(
            ZoneInfo(
                self.hass.config.time_zone
            )
        )


        result = {
            "latitude":
                match.latitude,

            "longitude":
                match.longitude,

            "drive_distance":
                drive_distance,

            "drive_time":
                drive_time,

            "arrival_time":
                planning[
                    "arrival_time"
                ],

            "departure_time":
                planning[
                    "departure_time"
                ],

            "travel_buffer":
                planning[
                    "travel_buffer"
                ],

            "arrival_buffer":
                planning[
                    "arrival_buffer"
                ],

            "updated":
                now,
        }


        #
        # RAM cache bijwerken.
        #

        self._travel_cache[
            match.match_id
        ] = result


        #
        # Persistent opslaan.
        #

        await self._async_save_travel_cache()


        return result


    #
    # ---------------------------------------------------------
    # COORDINATOR UPDATE
    # ---------------------------------------------------------
    #

    async def _async_update_data(
        self,
    ):
        """Haal KNBSB programma en reisinformatie op."""


        #
        # Cache slechts eenmaal na HA-start laden.
        #

        if not self._travel_cache_loaded:

            await self._async_load_travel_cache()

            self._travel_cache_loaded = True


        #
        # KNBSB wedstrijden ophalen.
        #

        matches = await self.api.get_matches()


        next_match = (
            matches[0]
            if matches
            else None
        )


        #
        # Oude cache-items verwijderen.
        #

        active_match_ids = {
            match.match_id
            for match in matches
        }


        stale_match_ids = [
            match_id
            for match_id
            in self._travel_cache
            if match_id
            not in active_match_ids
        ]


        if stale_match_ids:

            for match_id in stale_match_ids:

                self._travel_cache.pop(
                    match_id,
                    None,
                )


            await self._async_save_travel_cache()



        #
        # Travel data huidige wedstrijden.
        #

        match_travel = {}


        home = self.hass.states.get(
            "zone.home"
        )


        if home and matches:

            home_lat = float(
                home.attributes[
                    "latitude"
                ]
            )

            home_lon = float(
                home.attributes[
                    "longitude"
                ]
            )


            now = datetime.now(
                ZoneInfo(
                    self.hass.config.time_zone
                )
            )


            for index, match in enumerate(
                matches
            ):

                force_refresh = False


                match_dt = (
                    self._get_match_datetime(
                        match
                    )
                )


                time_until_match = (
                    match_dt - now
                )


                #
                # Alleen eerstvolgende wedstrijd:
                #
                # binnen 6 uur
                # +
                # cache ouder dan 30 minuten
                #
                # → ORS opnieuw ophalen.
                #

                if (
                    index == 0
                    and timedelta(0)
                    <= time_until_match
                    <= timedelta(hours=6)
                ):

                    cached = (
                        self._travel_cache.get(
                            match.match_id
                        )
                    )


                    if cached is None:

                        force_refresh = True

                    else:

                        updated = cached.get(
                            "updated"
                        )


                        if updated is None:

                            force_refresh = True

                        else:

                            cache_age = (
                                now - updated
                            )


                            if (
                                cache_age
                                >= timedelta(
                                    minutes=30
                                )
                            ):

                                force_refresh = True


                travel = (
                    await self._async_get_match_travel(
                        match,
                        home_lat,
                        home_lon,
                        force_refresh=force_refresh,
                    )
                )


                if travel:

                    match_travel[
                        match.match_id
                    ] = travel


        #
        # Next-match compatibility.
        #
        # Hierdoor blijven bestaande sensors
        # gewoon werken.
        #

        next_travel = None


        if next_match:

            next_travel = (
                match_travel.get(
                    next_match.match_id
                )
            )


        drive_distance = (
            next_travel.get(
                "drive_distance"
            )
            if next_travel
            else None
        )


        drive_time = (
            next_travel.get(
                "drive_time"
            )
            if next_travel
            else None
        )


        arrival_time = (
            next_travel.get(
                "arrival_time"
            )
            if next_travel
            else None
        )


        departure_time = (
            next_travel.get(
                "departure_time"
            )
            if next_travel
            else None
        )


        return {
            "matches":
                matches,

            "next_match":
                next_match,

            "match_travel":
                match_travel,

            "drive_distance":
                drive_distance,

            "drive_time":
                drive_time,

            "arrival_time":
                arrival_time,

            "departure_time":
                departure_time,
        }
