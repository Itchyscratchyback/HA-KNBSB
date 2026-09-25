from datetime import timedelta


DOMAIN = "knbsb"

CONF_TEAM_URL = "team_url"
CONF_ORS_API_KEY = "ors_api_key"

CONF_AWAY_ARRIVAL_MINUTES = (
    "away_arrival_minutes"
)

CONF_HOME_ARRIVAL_MINUTES = (
    "home_arrival_minutes"
)

UPDATE_INTERVAL = timedelta(
    hours=6
)

TRAVEL_BUFFER_PERCENT = 30
PARKING_BUFFER_MINUTES = 5


DEFAULT_HEADERS = {
    "Accept":
        "application/json, text/plain, */*",

    "Origin":
        "https://www.knbsb.nl",

    "Referer":
        "https://www.knbsb.nl/",

    "User-Agent":
        "HomeAssistant-KNBSB/1.0",

    "x-federationid":
        "d82c5610-66b2-4939-9897-8dac34becfc5",
}