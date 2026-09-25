from math import atan2, cos, radians, sin, sqrt

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    coordinator = entry.runtime_data

    async_add_entities(
        [
            KNBSBNextMatchSensor(coordinator),
            KNBSBNextMatchDateSensor(coordinator),
            KNBSBNextMatchTimeSensor(coordinator),
            KNBSBNextMatchLocationSensor(coordinator),
            KNBSBNextMatchLogoSensor(coordinator),
            KNBSBNextMatchAddressSensor(coordinator),
            KNBSBMatchesRemainingSensor(coordinator),
            KNBSBScheduleSensor(coordinator),
            KNBSBHomeAwaySensor(coordinator),
            KNBSBDistanceSensor(hass, coordinator),
            KNBSBDriveDistanceSensor(coordinator),
            KNBSBDriveTimeSensor(coordinator),
            KNBSBDepartureTimeSensor(coordinator),
            KNBSBArrivalTimeSensor(coordinator),
            KNBSBTeamNameSensor(coordinator),
            KNBSBTeamLogoSensor(coordinator),
            KNBSBOpponentNameSensor(coordinator),
            KNBSBOpponentLogoSensor(coordinator),
        ]
    )


class KNBSBBaseSensor(CoordinatorEntity, SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)

    @property
    def next_match(self):
        return self.coordinator.data.get("next_match")

    @property
    def matches(self):
        return self.coordinator.data.get(
            "matches",
            [],
        )


class KNBSBNextMatchSensor(KNBSBBaseSensor):

    @property
    def unique_id(self):
        return "knbsb_next_match"

    @property
    def name(self):
        return "KNBSB Next Match"

    @property
    def native_value(self):
        if not self.next_match:
            return "No Matches"

        return self.next_match.opponent

    @property
    def extra_state_attributes(self):
        if not self.next_match:
            return {}

        return {
            "date": self.next_match.date,
            "time": self.next_match.time,
            "location": self.next_match.location,
            "competition": self.next_match.competition,
            "home_away": self.next_match.home_away,
            "is_home_match":
                self.next_match.home_away == "Thuis",
        }


class KNBSBNextMatchDateSensor(KNBSBBaseSensor):

    @property
    def unique_id(self):
        return "knbsb_next_match_date"

    @property
    def name(self):
        return "KNBSB Next Match Date"

    @property
    def native_value(self):
        if not self.next_match:
            return None

        return self.next_match.date


class KNBSBNextMatchTimeSensor(KNBSBBaseSensor):

    @property
    def unique_id(self):
        return "knbsb_next_match_time"

    @property
    def name(self):
        return "KNBSB Next Match Time"

    @property
    def native_value(self):
        if not self.next_match:
            return None

        return self.next_match.time


class KNBSBNextMatchLocationSensor(KNBSBBaseSensor):

    @property
    def unique_id(self):
        return "knbsb_next_match_location"

    @property
    def name(self):
        return "KNBSB Next Match Location"

    @property
    def native_value(self):
        if not self.next_match:
            return None

        return self.next_match.location


class KNBSBNextMatchLogoSensor(KNBSBBaseSensor):

    @property
    def unique_id(self):
        return "knbsb_next_match_logo"

    @property
    def name(self):
        return "KNBSB Next Match Logo"

    @property
    def native_value(self):
        if not self.next_match:
            return None

        if self.next_match.home_away == "Thuis":
            return self.next_match.away_logo

        return self.next_match.home_logo

    @property
    def extra_state_attributes(self):
        if not self.next_match:
            return {}

        return {
            "opponent": self.next_match.opponent,
        }


class KNBSBNextMatchAddressSensor(KNBSBBaseSensor):

    @property
    def unique_id(self):
        return "knbsb_next_match_address"

    @property
    def name(self):
        return "KNBSB Next Match Address"

    @property
    def native_value(self):
        if not self.next_match:
            return None

        addr = self.next_match.address

        street = addr.get("address1", "")
        house_number = addr.get("houseNumber", "")
        extension = addr.get(
            "houseNumberExtension",
            "",
        )
        city = addr.get("city", "")

        street_line = " ".join(
            value
            for value in [
                street,
                f"{house_number}{extension}"
                if house_number
                else "",
            ]
            if value
        )

        return ", ".join(
            value
            for value in [
                street_line,
                city,
            ]
            if value
        )

    @property
    def extra_state_attributes(self):
        if not self.next_match:
            return {}

        addr = self.next_match.address

        return {
            "zip_code": addr.get("zipCode"),
            "country": addr.get("country"),
            "latitude": addr.get("latitude"),
            "longitude": addr.get("longitude"),
        }


class KNBSBMatchesRemainingSensor(KNBSBBaseSensor):

    @property
    def unique_id(self):
        return "knbsb_matches_remaining"

    @property
    def name(self):
        return "KNBSB Matches Remaining"

    @property
    def native_value(self):
        return len(self.matches)


class KNBSBHomeAwaySensor(KNBSBBaseSensor):

    @property
    def unique_id(self):
        return "knbsb_next_match_home_away"

    @property
    def name(self):
        return "KNBSB Next Match Home Away"

    @property
    def native_value(self):
        if not self.next_match:
            return None

        return self.next_match.home_away


class KNBSBDistanceSensor(KNBSBBaseSensor):

    def __init__(
        self,
        hass,
        coordinator,
    ):
        super().__init__(coordinator)

        self.hass = hass

    @property
    def unique_id(self):
        return "knbsb_next_match_distance"

    @property
    def name(self):
        return "KNBSB Next Match Distance"

    @property
    def native_unit_of_measurement(self):
        return "km"

    @property
    def extra_state_attributes(self):
        if not self.next_match:
            return {}

        home = self.hass.states.get(
            "zone.home"
        )

        if home is None:
            return {}

        return {
            "home_latitude":
                home.attributes.get(
                    "latitude"
                ),
            "home_longitude":
                home.attributes.get(
                    "longitude"
                ),
            "match_latitude":
                self.next_match.latitude,
            "match_longitude":
                self.next_match.longitude,
        }

    @property
    def native_value(self):
        if not self.next_match:
            return None

        home = self.hass.states.get(
            "zone.home"
        )

        if home is None:
            return None

        home_lat = home.attributes.get(
            "latitude"
        )
        home_lon = home.attributes.get(
            "longitude"
        )

        if (
            home_lat is None
            or home_lon is None
        ):
            return None

        match_lat = self.next_match.latitude
        match_lon = self.next_match.longitude

        radius = 6371.0

        dlat = radians(
            match_lat - home_lat
        )

        dlon = radians(
            match_lon - home_lon
        )

        a = (
            sin(dlat / 2) ** 2
            + cos(radians(home_lat))
            * cos(radians(match_lat))
            * sin(dlon / 2) ** 2
        )

        c = 2 * atan2(
            sqrt(a),
            sqrt(1 - a),
        )

        return round(
            radius * c,
            1,
        )


class KNBSBDriveDistanceSensor(KNBSBBaseSensor):

    @property
    def unique_id(self):
        return "knbsb_drive_distance"

    @property
    def name(self):
        return "KNBSB Drive Distance"

    @property
    def native_unit_of_measurement(self):
        return "km"

    @property
    def native_value(self):
        return self.coordinator.data.get(
            "drive_distance"
        )


class KNBSBDriveTimeSensor(KNBSBBaseSensor):

    @property
    def unique_id(self):
        return "knbsb_drive_time"

    @property
    def name(self):
        return "KNBSB Drive Time"

    @property
    def native_unit_of_measurement(self):
        return "min"

    @property
    def native_value(self):
        return self.coordinator.data.get(
            "drive_time"
        )


class KNBSBDepartureTimeSensor(KNBSBBaseSensor):

    @property
    def unique_id(self):
        return "knbsb_departure_time"

    @property
    def name(self):
        return "KNBSB Departure Time"

    @property
    def native_value(self):
        departure = (
            self.coordinator.data.get(
                "departure_time"
            )
        )

        if not departure:
            return None

        return departure.strftime(
            "%H:%M"
        )

    @property
    def extra_state_attributes(self):
        departure = (
            self.coordinator.data.get(
                "departure_time"
            )
        )

        if not departure:
            return {}

        return {
            "full_datetime":
                departure.isoformat(),
        }


class KNBSBArrivalTimeSensor(KNBSBBaseSensor):

    @property
    def unique_id(self):
        return "knbsb_arrival_time"

    @property
    def name(self):
        return "KNBSB Arrival Time"

    @property
    def native_value(self):
        arrival = (
            self.coordinator.data.get(
                "arrival_time"
            )
        )

        if not arrival:
            return None

        return arrival.strftime(
            "%H:%M"
        )

    @property
    def extra_state_attributes(self):
        arrival = (
            self.coordinator.data.get(
                "arrival_time"
            )
        )

        if not arrival:
            return {}

        return {
            "full_datetime":
                arrival.isoformat(),
        }


class KNBSBTeamNameSensor(KNBSBBaseSensor):

    @property
    def unique_id(self):
        return "knbsb_team_name"

    @property
    def name(self):
        return "KNBSB Team Name"

    @property
    def native_value(self):
        if not self.next_match:
            return None

        return self.next_match.team_name


class KNBSBTeamLogoSensor(KNBSBBaseSensor):

    @property
    def unique_id(self):
        return "knbsb_team_logo"

    @property
    def name(self):
        return "KNBSB Team Logo"

    @property
    def native_value(self):
        if not self.next_match:
            return None

        return self.next_match.team_logo


class KNBSBOpponentNameSensor(KNBSBBaseSensor):

    @property
    def unique_id(self):
        return "knbsb_opponent_name"

    @property
    def name(self):
        return "KNBSB Opponent Name"

    @property
    def native_value(self):
        if not self.next_match:
            return None

        return self.next_match.opponent_name


class KNBSBOpponentLogoSensor(KNBSBBaseSensor):

    @property
    def unique_id(self):
        return "knbsb_opponent_logo"

    @property
    def name(self):
        return "KNBSB Opponent Logo"

    @property
    def native_value(self):
        if not self.next_match:
            return None

        return self.next_match.opponent_logo


class KNBSBScheduleSensor(KNBSBBaseSensor):

    @staticmethod
    def clean_logo(value):
        if not value:
            return ""

        value = str(value)

        start = value.find('href="')

        if start != -1:
            start += 6

            end = value.find(
                '"',
                start,
            )

            if end != -1:
                return value[start:end]

        return value

    @staticmethod
    def format_address(address):
        if not address:
            return ""

        address_parts = []

        street = address.get(
            "address1"
        )
        house_number = address.get(
            "houseNumber"
        )
        extension = address.get(
            "houseNumberExtension"
        )

        if street:
            street_line = street

            if house_number:
                street_line += (
                    f" {house_number}"
                )

            if extension:
                street_line += str(
                    extension
                )

            address_parts.append(
                street_line
            )

        zip_code = address.get(
            "zipCode"
        )
        city = address.get(
            "city"
        )

        city_line = " ".join(
            part
            for part in [
                zip_code,
                city,
            ]
            if part
        )

        if city_line:
            address_parts.append(
                city_line
            )

        return ", ".join(
            address_parts
        )

    @property
    def unique_id(self):
        return "knbsb_schedule"

    @property
    def name(self):
        return "KNBSB Schedule"

    @property
    def native_value(self):
        return (
            f"{len(self.matches)} matches"
        )

    @property
    def extra_state_attributes(self):
        schedule = []

        travel_data = (
            self.coordinator.data.get(
                "match_travel",
                {},
            )
        )

        for match in self.matches:
            travel = travel_data.get(
                match.match_id,
                {},
            )

            formatted_address = (
                self.format_address(
                    match.address
                )
            )

            arrival_time = travel.get(
                "arrival_time"
            )

            departure_time = travel.get(
                "departure_time"
            )

            schedule.append(
                {
                    "match_id":
                        match.match_id,

                    "date":
                        match.date,

                    "time":
                        match.time,

                    "team_name":
                        match.team_name,

                    "team_logo":
                        self.clean_logo(
                            match.team_logo
                        ),

                    "opponent":
                        match.opponent,

                    "opponent_name":
                        match.opponent_name,

                    "opponent_logo":
                        self.clean_logo(
                            match.opponent_logo
                        ),

                    "home_team_name":
                        match.home_team_name,

                    "home_team_logo":
                        self.clean_logo(
                            match.home_team_logo
                        ),

                    "away_team_name":
                        match.away_team_name,

                    "away_team_logo":
                        self.clean_logo(
                            match.away_team_logo
                        ),

                    "home_away":
                        match.home_away,

                    "competition":
                        match.competition,

                    "location":
                        match.location,

                    "address":
                        formatted_address,

                    "latitude":
                        match.latitude,

                    "longitude":
                        match.longitude,

                    "drive_distance":
                        travel.get(
                            "drive_distance"
                        ),

                    "drive_time":
                        travel.get(
                            "drive_time"
                        ),

                    "arrival_time":
                        (
                            arrival_time.strftime(
                                "%H:%M"
                            )
                            if arrival_time
                            else None
                        ),

                    "departure_time":
                        (
                            departure_time.strftime(
                                "%H:%M"
                            )
                            if departure_time
                            else None
                        ),
                }
            )

        return {
            "matches":
                schedule,

            "match_count":
                len(schedule),

            "has_logos":
                all(
                    match.get(
                        "home_team_logo"
                    )
                    and
                    match.get(
                        "away_team_logo"
                    )
                    for match in schedule
                ),

            "has_travel_info":
                all(
                    match.get(
                        "drive_time"
                    )
                    is not None
                    for match in schedule
                ),
        }