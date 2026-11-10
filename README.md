# KNBSB voor Home Assistant

Een custom Home Assistant-integratie voor KNBSB-competities.

Hoofdpunten van deze integratie:

- Wedstrijdinformatie
-    Uitslagen
-    Competitie stand
-    Notities bij wedstrijden
-    Heatmap bij wedstrijden
-    locaties
- kalender integratie
- reisinformatie
-   Afstand in KM
-   Reistijd in minuten
-   Geplande vertrektijd vanaf "zone.home"
-   Geplande aankomst tijd op locatie
-   Instelbare tijd aanwezig voor wedstrijden thuis of uit (wordt meegenomen in vertrektijd)
-   One click Navigatie knop via de meegeleverde KNBSB Schedule card
-   Navigatie via Android Auto | Apple carplay Homeassistant  Kies: **Navigatie** -> **knbsb_next_match_address**
-   Uitslagen, standen, notities en heatmaps worden opgeslagen in `.storage/knbsb.history` en getoond in de dashboardkaart.

Voor rijafstand en reistijd wordt OpenRouteService.org gebruikt. Dit is een gratis service waar moet registreren voor een eigen API key.

> Dit is een onofficiële community-integratie en is niet verbonden aan of goedgekeurd door de KNBSB.

## Installatie via HACS

1. Zoek **KNBSB** in HACS, download de integratie en herstart Home Assistant.
2. Ga naar **Instellingen > Apparaten & services > Integratie toevoegen** en kies **KNBSB**.
3. Vul in:
   - **KNBSB Team URL**: zie hieronder.
   - **OpenRouteService API-sleutel**: zie hieronder.
   - **Tijd vooraf aanwezig** bij uit- en thuiswedstrijden (in minuten; er wordt automatisch 5 minuten parkeertijd bij opgeteld).
4. Wil je meerdere teams volgen? Voeg de integratie opnieuw toe met de URL van het andere team.

De integratie controleert de URL en haalt bij het toevoegen meteen de wedstrijden op. Bij een foute URL of onbereikbare API zie je direct een foutmelding.

### De team-URL vinden

1. Ga naar [knbsb.nl/competities/teams](https://www.knbsb.nl/competities/teams/) en open de pagina van je team.
2. Kies **Programma** en kopieer de URL uit de adresbalk. Die moet er zo uitzien:

```
https://www.knbsb.nl/competities/teams/#/clubs/<club-id>/teams/<team-id>/program?poolId=<poule-nummer>
```

### OpenRouteService API-sleutel

1. Maak een gratis account op [openrouteservice.org](https://openrouteservice.org/dev/#/signup).
2. Maak onder **Dashboard > Request a token** een token aan van het type *Free*.
3. Plak dit token in het veld **OpenRouteService API-sleutel**.

> **Privacy:** voor de routeberekening worden de coördinaten van je thuislocatie (`zone.home`) en van de wedstrijdlocaties naar OpenRouteService (HeiGIT, `api.heigit.org`) gestuurd. Andere gegevens worden daarheen niet verstuurd.

### Dashboardkaart

De kaart zit in de integratie (`custom_components/knbsb/www/`) en wordt bij het opstarten automatisch geladen; je hoeft geen aparte resource of HACS-plugin toe te voegen. 
Voeg de kaart toe aan een dashboard met type `custom:knbsb-schedule-card`.


Zie hieronder de view die de integratie ondersteunt samen met de meegeleverde KNBSB Schedule card

---
### Onderstaande is mogelijk met de KNBSB Schedule card (meegeleverd)
<img width="130%" height="130%" alt="screenshot-3" src="https://github.com/user-attachments/assets/7b0201b6-5469-4009-b607-ed334743df44"/>


<img width="40%" height="40%" alt="image" src="https://github.com/user-attachments/assets/c73918ce-8947-4ca7-83d4-c0f5461aa4a9" /> <img width="40%" height="40%" alt="image" src="https://github.com/user-attachments/assets/ed827cf2-155c-4326-a306-37ea9293fa64" />

<img width="40%" height="40%" alt="uitslagen" src="https://github.com/user-attachments/assets/11e937d2-0b37-470a-8ce5-2a518dcec1fe" />

<img width="40%" height="40%" alt="heatmap" src="https://github.com/user-attachments/assets/e39652a2-bd78-4820-b9b3-bc99c1d2215e" />

<img width="40%" height="40%" alt="competitie-stand" src="https://github.com/user-attachments/assets/c04cade5-e38a-4b2b-a65e-e362b2dbd559" />

## Functionaliteit

## Navigatie via Homeassistant in AndroidAuto (getest) of CarPlay (ongetest)
Deze integratie levert een sensor die door HA in AA modus kan worden gebruikt als navigatie actie

In AndroidAuto modus open; Homeassistant -> Navigation -> Kies de Match

Zie hieronder een voorbeeld van een match:

<img width="20%" height="20%" alt="HA-AA-Navigatie-knop" src="https://github.com/user-attachments/assets/e1fc0dae-9ab9-4491-be40-2f5f7244ae53" />

---
