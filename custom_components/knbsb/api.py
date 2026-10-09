import logging
import re

from datetime import date

from .const import (
    DEFAULT_HEADERS,

)

from .models import Match

_LOGGER = logging.getLogger(__name__)


class FoysApi:

    def __init__(
        self,
        session,
        organisation_id,
        team_guid,
        pool_id,
        ors_api_key,
    ):
        self.session = session
        self.organisation_id = organisation_id
        self.team_guid = team_guid
        self.pool_id = pool_id
        self.ors_api_key = ors_api_key

    async def get_drive_info(
        self,
        home_lat,
        home_lon,
        match_lat,
        match_lon,
    ):

        url = (
            "https://api.heigit.org/"
            "openrouteservice/v2/directions/driving-car"
        )

        headers = {
            "Authorization": self.ors_api_key,
            "Content-Type": "application/json",
        }

        payload = {
            "coordinates": [
                [home_lon, home_lat],
                [match_lon, match_lat],
            ]
        }


        async with self.session.post(
            url,
            headers=headers,
            json=payload,
        ) as response:

            try:

                data = await response.json()

            except Exception as err:

                text = await response.text()

                raise


            if response.status != 200:

                raise Exception(
                    f"ORS Error {response.status}: {data}"
                )

            if "routes" not in data:

                raise Exception(
                    f"Unexpected ORS response: {data}"
                )

        summary = data["routes"][0]["summary"]


        return {
            "distance_km": round(
                summary["distance"] / 1000,
                1,
            ),
            "duration_min": round(
                summary["duration"] / 60,
            ),
        }

    async def get_matches(self):

        url = (
            "https://api.foys.io/"
            "competition/public-api/v1/matches"
        )

        params = {
            "startDate": date.today().isoformat(),
            "organisationId": self.organisation_id,
            "teamGuid": self.team_guid,
            "poolId": self.pool_id,
            "skipCount": 0,
            "maxResultCount": 100,
            "sorting": "date asc, startTime asc",
        }


        async with self.session.get(
            url,
            params=params,
            headers=DEFAULT_HEADERS,
        ) as response:

            response.raise_for_status()

            data = await response.json()


        matches = []

        for item in data.get("items", []):

            is_home = (
                item["homeTeamGuid"]
                == self.team_guid
            )

            # Objectieve wedstrijdvolgorde.
            # Deze waarden moeten voor ELKE wedstrijd
            # opnieuw uit het huidige item komen.

            home_club_name = (
                item[
                    "homeOrganisation"
                ]["name"]
            )

            home_team_name = (
                item.get(
                    "homeTeamName"
                )
                or home_club_name
            )

            home_team_logo = (
                item["homeLogoUrl"]
            )


            away_club_name = (
                item[
                    "awayOrganisation"
                ]["name"]
            )

            away_team_name = (
                item.get(
                    "awayTeamName"
                )
                or away_club_name
            )

            away_team_logo = (
                item["awayLogoUrl"]
            )

            # Gegevens vanuit het perspectief
            # van het gevolgde team.

            if is_home:

                team_club_name = (
                    home_club_name
                )

                team_name = (
                    home_team_name
                )

                team_logo = (
                    home_team_logo
                )

                opponent_club_name = (
                    away_club_name
                )

                opponent_name = (
                    away_team_name
                )

                opponent_logo = (
                    away_team_logo
                )

            else:

                team_club_name = (
                    away_club_name
                )

                team_name = (
                    away_team_name
                )

                team_logo = (
                    away_team_logo
                )

                opponent_club_name = (
                    home_club_name
                )

                opponent_name = (
                    home_team_name
                )

                opponent_logo = (
                    home_team_logo
                )

            matches.append(
                Match(
                    match_id=item["id"],

                    date=item["date"].split("T")[0],
                    time=item["startTime"][:5],

                    team_name=team_name,
                    team_logo=team_logo,
                    team_club_name=team_club_name,

                    opponent=opponent_name,
                    opponent_name=opponent_name,
                    opponent_logo=opponent_logo,
                    opponent_club_name=opponent_club_name,

                    home_team_name=home_team_name,
                    home_logo=item["homeLogoUrl"],
                    home_club_name=home_club_name,
                    home_team_logo=home_team_logo,

                    away_club_name=away_club_name,
                    away_team_name=away_team_name,
                    away_team_logo=away_team_logo,
                    away_logo=item["awayLogoUrl"],


                    location=item["accommodationName"],

                    competition=item["competition"]["name"],

                    home_away=(
                        "Thuis"
                        if is_home
                        else "Uit"
                    ),

                    address=item["address"],

                    latitude=item["address"]["latitude"],
                    longitude=item["address"]["longitude"],


                )
            )


        return matches

def parse_team_url(
    url: str,
):

    pattern = (
        r"clubs/"
        r"(?P<organisation>[0-9a-fA-F\-]+)"
        r"/teams/"
        r"(?P<team>[0-9a-fA-F\-]+)"
        r"/program\?poolId="
        r"(?P<pool>\d+)"
    )

    match = re.search(
        pattern,
        url,
    )

    if not match:

        raise ValueError(
            f"Invalid KNBSB URL: {url}"
        )

    return {
        "organisation_id":
            match.group(
                "organisation"
            ),

        "team_guid":
            match.group(
                "team"
            ),

        "pool_id":
            int(
                match.group(
                    "pool"
                )
            ),
    }