class KNBSBScheduleCard extends HTMLElement {

    setConfig(config) {

        if (!config.entity) {
            throw new Error(
                "KNBSB Schedule Card: entity is verplicht"
            );
        }

        this.config = config;
    }


    set hass(hass) {

        const entity =
            hass.states[this.config.entity];


        if (!entity) {

            this.innerHTML = `
                <ha-card class="message-card">
                    Entity niet gevonden:
                    ${this.config.entity}
                </ha-card>
            `;

            return;
        }


        const matches =
            entity.attributes.matches || [];


        if (matches.length === 0) {

            this.innerHTML = `
                <ha-card class="message-card">
                    Geen geplande wedstrijden
                </ha-card>
            `;

            return;
        }


        const matchCards = matches
            .map(
                (match, index) =>
                    this.renderMatch(
                        match,
                        index === 0
                    )
            )
            .join("");


        this.innerHTML = `

            <style>

                /*
                 * HOOFDCONTAINER
                 */

                .container {
                    padding: 8px;
                }


                /*
                 * TITEL
                 */

                .header {
                    margin-bottom: 24px;

                    text-align: center;

                    font-size: 26px;
                    font-weight: 700;
                }


                /*
                 * RESPONSIVE GRID
                 */

                .matches-grid {
                    display: grid;

                    grid-template-columns:
                        repeat(
                            auto-fit,
                            minmax(360px, 1fr)
                        );

                    gap: 16px;

                    align-items: stretch;
                }


                /*
                 * WEDSTRIJDKAART
                 */

                ha-card.match-card {
                    position: relative;

                    display: block;

                    height: 100%;

                    padding: 20px;

                    margin: 0;

                    box-sizing: border-box;

                    border-radius: 18px;
                }


                /*
                 * VOLGENDE WEDSTRIJD
                 */

                ha-card.match-card.next-match {
                    border:
                        2px solid
                        var(--primary-color);

                    box-shadow:
                        0 0 12px
                        color-mix(
                            in srgb,
                            var(--primary-color) 25%,
                            transparent
                        );
                }


                .next-match-badge {
                    display: inline-block;

                    margin-bottom: 14px;

                    padding: 5px 10px;

                    border-radius: 12px;

                    background:
                        var(--primary-color);

                    color:
                        var(--text-primary-color);

                    font-size: 11px;
                    font-weight: 700;

                    letter-spacing: 0.5px;

                    text-transform: uppercase;
                }


                /*
                 * MATCHUP
                 */

                .matchup {
                    display: grid;

                    grid-template-columns:
                        minmax(0, 1fr)
                        60px
                        minmax(0, 1fr);

                    align-items: center;

                    gap: 12px;
                }


                /*
                 * TEAM
                 */

                .team {
                    min-width: 0;

                    text-align: center;
                }


                .team-role {
                    margin-bottom: 8px;

                    font-size: 11px;
                    font-weight: 700;

                    letter-spacing: 0.8px;

                    text-transform: uppercase;

                    opacity: 0.65;
                }


                /*
                 * LOGO'S
                 */

                .logo-container {
                    height: 160px;

                    display: flex;

                    align-items: center;
                    justify-content: center;

                    margin-bottom: 10px;
                }


                .team-logo {
                    display: block;

                    width: 140px;
                    height: 140px;

                    max-width: 100%;

                    object-fit: contain;
                }


                .logo-placeholder {
                    width: 120px;
                    height: 120px;

                    display: flex;

                    align-items: center;
                    justify-content: center;

                    font-size: 48px;

                    opacity: 0.5;
                }


                /*
                 * TEAMNAAM
                 */

                .team-name {
                    font-size: 16px;
                    font-weight: 700;

                    line-height: 1.3;

                    white-space: normal;

                    overflow-wrap: normal;
                    word-break: normal;
                }


                /*
                 * VS
                 */

                .versus {
                    text-align: center;

                    font-size: 28px;
                    font-weight: 800;
                }


                /*
                 * WEDSTRIJDINFORMATIE
                 */

                .match-info {
                    margin-top: 20px;

                    padding-top: 16px;

                    border-top:
                        1px solid
                        var(--divider-color);

                    text-align: center;

                    line-height: 1.8;
                }


                .date-time {
                    display: flex;

                    justify-content: center;

                    flex-wrap: wrap;

                    gap: 18px;

                    font-size: 16px;
                    font-weight: 600;
                }


                .home-away {
                    margin-top: 4px;
                }


                /*
                 * LOCATIE
                 */

                .location-block {
                    margin-top: 10px;
                }


                .location {
                    font-weight: 600;
                }


                .address {
                    margin-top: 2px;

                    font-size: 13px;

                    opacity: 0.75;
                }


                /*
                 * REISINFORMATIE
                 */

                .travel-info {
                    display: flex;

                    justify-content: center;

                    flex-wrap: wrap;

                    gap: 10px 18px;

                    margin-top: 16px;

                    padding-top: 14px;

                    border-top:
                        1px solid
                        var(--divider-color);
                }


                .travel-item {
                    display: flex;

                    align-items: center;

                    gap: 6px;

                    font-size: 14px;
                }


                .travel-icon {
                    font-size: 16px;
                }


                /*
                 * PLANNING
                 */

                .planning-info {
                    margin-top: 14px;

                    padding: 12px 14px;

                    border-radius: 12px;

                    background:
                        color-mix(
                            in srgb,
                            var(--primary-color) 8%,
                            transparent
                        );
                }


                .planning-row {
                    display: flex;

                    justify-content: space-between;

                    align-items: center;

                    gap: 12px;

                    padding: 3px 0;

                    font-size: 14px;
                }


                .planning-row strong {
                    white-space: nowrap;

                    font-size: 15px;
                }


                /*
                 * NAVIGATIE
                 */

                .navigation-container {
                    display: flex;

                    justify-content: center;

                    margin-top: 16px;
                }


                .navigation-button {
                    display: inline-flex;

                    align-items: center;
                    justify-content: center;

                    min-width: 140px;

                    padding: 9px 18px;

                    border-radius: 18px;

                    background:
                        var(--primary-color);

                    color:
                        var(--text-primary-color);

                    text-decoration: none;

                    font-size: 14px;
                    font-weight: 700;

                    cursor: pointer;

                    transition:
                        filter 0.15s ease,
                        transform 0.15s ease;
                }


                .navigation-button:hover {
                    filter: brightness(1.08);

                    transform: translateY(-1px);
                }


                .navigation-button:active {
                    transform: translateY(0);
                }


                /*
                 * COMPETITIE
                 */

                .competition {
                    margin-top: 14px;

                    font-size: 13px;

                    opacity: 0.65;
                }


                /*
                 * EMPTY / ERROR
                 */

                ha-card.message-card {
                    padding: 20px;

                    text-align: center;
                }


                /*
                 * MOBIEL
                 */

                @media (max-width: 600px) {

                    .container {
                        padding: 4px;
                    }


                    .matches-grid {
                        grid-template-columns: 1fr;

                        gap: 12px;
                    }


                    ha-card.match-card {
                        padding: 14px;
                    }


                    .matchup {
                        grid-template-columns:
                            minmax(0, 1fr)
                            40px
                            minmax(0, 1fr);

                        gap: 5px;
                    }


                    .logo-container {
                        height: 110px;
                    }


                    .team-logo {
                        width: 100px;
                        height: 100px;
                    }


                    .team-name {
                        font-size: 14px;
                    }


                    .versus {
                        font-size: 20px;
                    }


                    .header {
                        margin-bottom: 16px;

                        font-size: 22px;
                    }


                    .date-time {
                        gap: 8px;

                        font-size: 14px;
                    }


                    .travel-info {
                        gap: 8px 12px;
                    }


                    .planning-info {
                        padding: 10px;
                    }


                    .planning-row {
                        gap: 8px;

                        font-size: 13px;
                    }


                    .planning-row strong {
                        font-size: 14px;
                    }


                    .address {
                        font-size: 12px;
                    }


                    .navigation-button {
                        width: 100%;

                        box-sizing: border-box;
                    }

                }

            </style>


            <div class="container">

                <div class="header">
                    ⚾ KNBSB Programma
                </div>


                <div class="matches-grid">
                    ${matchCards}
                </div>

            </div>
        `;
    }



    renderMatch(
        match,
        isNextMatch = false
    ) {

        /*
         * THUIS LINKS
         * UIT RECHTS
         */

        const homeTeamName =
            this.escapeHtml(
                match.home_team_name ||
                "Thuisteam"
            );


        const awayTeamName =
            this.escapeHtml(
                match.away_team_name ||
                "Uitteam"
            );


        const homeTeamLogo =
            this.normalizeUrl(
                match.home_team_logo
            );


        const awayTeamLogo =
            this.normalizeUrl(
                match.away_team_logo
            );


        /*
         * LOGO OPBOUW
         */

        let homeTeamLogoHtml;


        if (homeTeamLogo) {

            homeTeamLogoHtml =
                '<img ' +
                'class="team-logo" ' +
                'src="' +
                this.escapeAttribute(
                    homeTeamLogo
                ) +
                '" ' +
                'alt="' +
                this.escapeAttribute(
                    homeTeamName
                ) +
                ' logo" ' +
                'loading="lazy" ' +
                '>';

        } else {

            homeTeamLogoHtml = `
                <div class="logo-placeholder">
                    ⚾
                </div>
            `;
        }


        let awayTeamLogoHtml;


        if (awayTeamLogo) {

            awayTeamLogoHtml =
                '<img ' +
                'class="team-logo" ' +
                'src="' +
                this.escapeAttribute(
                    awayTeamLogo
                ) +
                '" ' +
                'alt="' +
                this.escapeAttribute(
                    awayTeamName
                ) +
                ' logo" ' +
                'loading="lazy" ' +
                '>';

        } else {

            awayTeamLogoHtml = `
                <div class="logo-placeholder">
                    ⚾
                </div>
            `;
        }


        /*
         * BASISGEGEVENS
         */

        const date =
            this.escapeHtml(
                match.date || ""
            );


        const time =
            this.escapeHtml(
                match.time || ""
            );


        const homeAway =
            this.escapeHtml(
                match.home_away || ""
            );


        const location =
            this.escapeHtml(
                match.location || ""
            );


        const address =
            this.escapeHtml(
                match.address || ""
            );


        const competition =
            this.escapeHtml(
                match.competition || ""
            );


        /*
         * REISGEGEVENS
         */

        const driveDistance =
            (
                match.drive_distance !== null &&
                match.drive_distance !== undefined
            )
                ? this.escapeHtml(
                    match.drive_distance
                )
                : "";


        const driveTime =
            (
                match.drive_time !== null &&
                match.drive_time !== undefined
            )
                ? this.escapeHtml(
                    match.drive_time
                )
                : "";


        const arrivalTime =
            this.escapeHtml(
                match.arrival_time || ""
            );


        const departureTime =
            this.escapeHtml(
                match.departure_time || ""
            );


        /*
         * COORDINATEN
         */

        const latitude =
            match.latitude;


        const longitude =
            match.longitude;


        const hasCoordinates =
            latitude !== null &&
            latitude !== undefined &&
            longitude !== null &&
            longitude !== undefined;


        /*
         * GOOGLE MAPS NAVIGATIE
         */

        const navigationUrl =
            hasCoordinates
                ? (
                    "https://www.google.com/maps/dir/?api=1" +
                    "&destination=" +
                    encodeURIComponent(
                        `${latitude},${longitude}`
                    ) +
                    "&travelmode=driving"
                )
                : "";


        /*
         * WEDSTRIJDKAART
         */

        return `

            <ha-card
                class="
                    match-card
                    ${isNextMatch
                ? "next-match"
                : ""
            }
                "
            >


                ${isNextMatch
                ? `
                            <div class="next-match-badge">
                                VOLGENDE WEDSTRIJD
                            </div>
                        `
                : ""
            }


                <div class="matchup">


                    <!-- THUIS -->


                    <div class="team">

                        <div class="team-role">
                            THUIS
                        </div>


                        <div class="logo-container">
                            ${homeTeamLogoHtml}
                        </div>


                        <div class="team-name">
                            ${homeTeamName}
                        </div>

                    </div>


                    <!-- VS -->


                    <div class="versus">
                        VS
                    </div>


                    <!-- UIT -->


                    <div class="team">

                        <div class="team-role">
                            UIT
                        </div>


                        <div class="logo-container">
                            ${awayTeamLogoHtml}
                        </div>


                        <div class="team-name">
                            ${awayTeamName}
                        </div>

                    </div>


                </div>


                <div class="match-info">


                    <!-- DATUM / TIJD -->


                    <div class="date-time">

                        <span>
                            🗓️ ${date}
                        </span>

                        <span>
                            🕒 ${time}
                        </span>

                    </div>


                    <!-- GEVOLGD TEAM -->


                    <div class="home-away">
                        🏟️ Gevolgd team: ${homeAway}
                    </div>


                    <!-- LOCATIE -->


                    <div class="location-block">

                        <div class="location">
                            📍 ${location}
                        </div>


                        ${address
                ? `
                                    <div class="address">
                                        ${address}
                                    </div>
                                `
                : ""
            }

                    </div>


                    <!-- AFSTAND / RIJTIJD -->


                    ${driveDistance || driveTime
                ? `
                                <div class="travel-info">


                                    ${driveDistance
                    ? `
                                                <div class="travel-item">

                                                    <span class="travel-icon">
                                                        🚗
                                                    </span>

                                                    <span>
                                                        ${driveDistance} km
                                                    </span>

                                                </div>
                                            `
                    : ""
                }


                                    ${driveTime
                    ? `
                                                <div class="travel-item">

                                                    <span class="travel-icon">
                                                        ⏱️
                                                    </span>

                                                    <span>
                                                        ${driveTime} minuten
                                                    </span>

                                                </div>
                                            `
                    : ""
                }


                                </div>
                            `
                : ""
            }


                    <!-- PLANNING -->


                    ${arrivalTime || departureTime
                ? `
                                <div class="planning-info">


                                    ${arrivalTime
                    ? `
                                                <div class="planning-row">

                                                    <span>
                                                        ✅ Geplande aankomst
                                                    </span>

                                                    <strong>
                                                        ${arrivalTime}
                                                    </strong>

                                                </div>
                                            `
                    : ""
                }


                                    ${departureTime
                    ? `
                                                <div class="planning-row">

                                                    <span>
                                                        🚙 Vertrek vanaf huis
                                                    </span>

                                                    <strong>
                                                        ${departureTime}
                                                    </strong>

                                                </div>
                                            `
                    : ""
                }


                                </div>
                            `
                : ""
            }


                    <!-- NAVIGATIE -->


                    ${navigationUrl
                ? `
                                <div class="navigation-container">

                                    <a
                                        class="navigation-button"
                                        href="${navigationUrl}"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        📍 Navigeer
                                    </a>

                                </div>
                            `
                : ""
            }


                    <!-- COMPETITIE -->


                    ${competition
                ? `
                                <div class="competition">
                                    ${competition}
                                </div>
                            `
                : ""
            }


                </div>


            </ha-card>
        `;
    }



    normalizeUrl(value) {

        if (!value) {
            return "";
        }


        const url =
            String(value).trim();


        if (
            url.startsWith(
                "https://"
            ) ||
            url.startsWith(
                "http://"
            )
        ) {
            return url;
        }


        return "";
    }



    escapeHtml(value) {

        return String(value)

            .replaceAll(
                "&",
                "&amp;"
            )

            .replaceAll(
                "<",
                "&lt;"
            )

            .replaceAll(
                ">",
                "&gt;"
            )

            .replaceAll(
                '"',
                "&quot;"
            )

            .replaceAll(
                "'",
                "&#039;"
            );
    }



    escapeAttribute(value) {

        return this.escapeHtml(
            value
        );
    }



    getCardSize() {

        return 6;
    }



    static getStubConfig() {

        return {
            entity:
                "sensor.knbsb_schedule"
        };
    }

}



if (
    !customElements.get(
        "knbsb-schedule-card"
    )
) {

    customElements.define(
        "knbsb-schedule-card",
        KNBSBScheduleCard
    );
}



window.customCards =
    window.customCards || [];



window.customCards.push({

    type:
        "knbsb-schedule-card",

    name:
        "KNBSB Schedule Card",

    description:
        "KNBSB programma met reistijd, planning en navigatie."

});