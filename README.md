# KNBSB voor Home Assistant

Een custom Home Assistant-integratie voor KNBSB-competities.

De integratie haalt het wedstrijdprogramma van een KNBSB-team op en maakt wedstrijdinformatie, locaties, kalenderafspraken en reisinformatie beschikbaar binnen Home Assistant.

Voor rijafstand en reistijd wordt OpenRouteService / HeiGIT gebruikt.

> Dit is een onofficiële community-integratie en is niet verbonden aan of goedgekeurd door de KNBSB.

---

<img width="515" height="694" alt="image" src="https://github.com/user-attachments/assets/c73918ce-8947-4ca7-83d4-c0f5461aa4a9" />

<img width="946" height="1218" alt="image" src="https://github.com/user-attachments/assets/ed827cf2-155c-4326-a306-37ea9293fa64" />



## Functionaliteit

### Wedstrijdinformatie

De integratie haalt het actuele en toekomstige wedstrijdprogramma op van het ingestelde KNBSB-team.

Beschikbare informatie omvat onder andere:

- Volgende tegenstander
- Wedstrijddatum
- Wedstrijdtijd
- Thuis / Uit
- Competitie
- Wedstrijdlocatie
- Adres
- Thuisteam
- Uitteam
- Teamlogo's
- Aantal resterende wedstrijden
- Volledig wedstrijdprogramma

---

## Kalender

Er wordt automatisch een Home Assistant kalenderentity aangemaakt met alle toekomstige wedstrijden.

```text
calendar.knbsb_team
```

Wedstrijdtijden worden verwerkt in:

```text
Europe/Amsterdam
```

Hierdoor wordt automatisch rekening gehouden met Nederlandse zomer- en wintertijd.

---

## Reisinformatie

Voor iedere geplande wedstrijd kan reisinformatie worden berekend vanaf:

```text
zone.home
```

naar de wedstrijdlocatie.

Hiervoor wordt OpenRouteService / HeiGIT gebruikt.

Beschikbare informatie:

- Rijafstand
- Reistijd
- Geplande aankomsttijd
- Vertrektijd
- Hemelsbrede afstand

De routegegevens van wedstrijden worden persistent opgeslagen zodat Home Assistant na een herstart niet het volledige programma opnieuw hoeft te berekenen.

---

## Berekening van de vertrektijd

De vertrektijd bestaat uit:

```text
Rijtijd
+ 30% reistijdbuffer
+ ingestelde aanwezigheidstijd
+ 5 minuten parkeertijd
```

Voor thuis- en uitwedstrijden kunnen afzonderlijke aanwezigheidstijden worden ingesteld.

### Voorbeeld

```text
Wedstrijdtijd:             10:00
Rijtijd:                   32 minuten
Reisbuffer 30%:            10 minuten
Vooraf aanwezig:           30 minuten
Parkeren:                   5 minuten
```

Geplande aankomst:

```text
09:25
```

Vertrek vanaf huis:

```text
08:43
```

---

# Vereisten

## Home Assistant

Een recente versie van Home Assistant wordt aanbevolen.

## OpenRouteService API-sleutel

Voor de berekening van rijafstand en reistijd is een persoonlijke OpenRouteService / HeiGIT API-sleutel nodig.

Iedere installatie moet een eigen API-sleutel gebruiken.

Deel geen API-sleutel tussen meerdere gebruikers of Home Assistant-installaties.

---

# Installatie via HACS

Deze beta kan via HACS als custom repository worden geïnstalleerd.

## Stap 1

Open HACS in Home Assistant.

## Stap 2

Open:

```text
HACS
→ Integraties
→ Custom repositories
```

## Stap 3

Voeg deze repository toe:

```text
https://github.com/Itchyscratchyback/HA-KNBSB
```

Selecteer als type:

```text
Integration
```

## Stap 4

Installeer:

```text
KNBSB
```

## Stap 5

Herstart Home Assistant.

---

# Configuratie

Na de herstart:

```text
Instellingen
→ Apparaten & diensten
→ Integratie toevoegen
```

Zoek naar:

```text
KNBSB
```

Tijdens de configuratie worden vier gegevens gevraagd.

---

## KNBSB Team URL

Open op de KNBSB-website het programma van het gewenste team.

De URL lijkt bijvoorbeeld op:

```text
https://www.knbsb.nl/competities/teams/#/clubs/<organisatie-id>/teams/<team-id>/program?poolId=<poule-id>
```

Plak de volledige URL in de KNBSB-configuratie.

De integratie bepaalt automatisch:

- Organisatie-ID
- Team-ID
- Poule-ID

Deze gegevens hoeven dus niet afzonderlijk ingevoerd te worden.

---

## OpenRouteService API-sleutel

Voer de persoonlijke OpenRouteService / HeiGIT API-sleutel in.

Deze wordt gebruikt voor het berekenen van autoroutes.

---

## Vooraf aanwezig bij uitwedstrijd

Het aantal minuten dat je vóór een uitwedstrijd aanwezig wilt zijn.

Bijvoorbeeld:

```text
30 minuten
```

De integratie telt automatisch:

```text
+5 minuten parkeren
```

bij deze tijd op.

---

## Vooraf aanwezig bij thuiswedstrijd

Het aantal minuten dat je vóór een thuiswedstrijd aanwezig wilt zijn.

Bijvoorbeeld:

```text
15 minuten
```

Ook hier wordt automatisch:

```text
+5 minuten parkeren
```

meegerekend.

---

# Entities

De integratie maakt momenteel de volgende entities aan.

## Volgende wedstrijd

```text
sensor.knbsb_next_match
```

Toont de tegenstander van de eerstvolgende wedstrijd.

---

## Datum

```text
sensor.knbsb_next_match_date
```

---

## Tijd

```text
sensor.knbsb_next_match_time
```

---

## Thuis / Uit

```text
sensor.knbsb_next_match_home_away
```

Waarde:

```text
Thuis
```

of:

```text
Uit
```

---

## Wedstrijdlocatie

```text
sensor.knbsb_next_match_location
```

---

## Wedstrijdadres

```text
sensor.knbsb_next_match_address
```

---

## Logo volgende tegenstander

```text
sensor.knbsb_next_match_logo
```

---

## Teamnaam

```text
sensor.knbsb_team_name
```

---

## Teamlogo

```text
sensor.knbsb_team_logo
```

---

## Naam tegenstander

```text
sensor.knbsb_opponent_name
```

---

## Logo tegenstander

```text
sensor.knbsb_opponent_logo
```

---

## Hemelsbrede afstand

```text
sensor.knbsb_next_match_distance
```

Afstand vanaf `zone.home` naar de wedstrijdlocatie.

Eenheid:

```text
km
```

Dit is geen autoroute.

---

## Rijafstand

```text
sensor.knbsb_drive_distance
```

Berekend via OpenRouteService.

---

## Reistijd

```text
sensor.knbsb_drive_time
```

Eenheid:

```text
min
```

---

## Geplande aankomsttijd

```text
sensor.knbsb_arrival_time
```

---

## Vertrektijd vanaf huis

```text
sensor.knbsb_departure_time
```

---

## Resterende wedstrijden

```text
sensor.knbsb_matches_remaining
```

---

# Volledig wedstrijdprogramma

```text
sensor.knbsb_schedule
```

Deze sensor bevat het volledige toekomstige wedstrijdprogramma in het attribuut:

```text
matches
```

Iedere wedstrijd bevat onder andere:

```yaml
match_id:
date:
time:

home_team_name:
home_team_logo:

away_team_name:
away_team_logo:

home_away:
competition:

location:
address:
latitude:
longitude:

drive_distance:
drive_time:

arrival_time:
departure_time:
```

Deze gegevens kunnen worden gebruikt voor eigen dashboards en automatiseringen.

---

# KNBSB Kalender

```text
calendar.knbsb_team
```

De kalender bevat alle toekomstige wedstrijden van het ingestelde team.

---

# KNBSB Schedule Card

Voor deze integratie wordt ook een aparte Home Assistant dashboardkaart ontwikkeld:

```text
KNBSB Schedule Card
```

De kaart wordt als een **afzonderlijke HACS frontend-repository** gepubliceerd.

De kaart ondersteunt onder andere:

- Losse kaart per wedstrijd
- Thuisteam links
- Uitteam rechts
- Teamlogo's
- Responsive layout
- Markering van de eerstvolgende wedstrijd
- Wedstrijdlocatie
- Adres
- Rijafstand
- Reistijd
- Geplande aankomst
- Vertrektijd
- Navigatie via Google Maps

De KNBSB backend-integratie kan ook volledig zonder deze kaart worden gebruikt.

De repositorylink van de KNBSB Schedule Card wordt toegevoegd zodra de aparte card-release beschikbaar is.

---

# Route-cache

OpenRouteService routegegevens worden persistent opgeslagen door Home Assistant.

Hierdoor hoeven na iedere Home Assistant-herstart niet opnieuw routes voor het volledige wedstrijdprogramma berekend te worden.

Een bestaande route wordt hergebruikt zolang:

- de wedstrijdlocatie niet verandert;
- de route nog in de cache beschikbaar is.

Voor de eerstvolgende wedstrijd wordt de route opnieuw gecontroleerd wanneer:

```text
de wedstrijd binnen 6 uur plaatsvindt
```

en:

```text
de opgeslagen route minimaal 30 minuten oud is
```

Hierdoor blijft de reisinformatie vlak voor een wedstrijd actueel zonder onnodig veel API-verzoeken uit te voeren.

---

# Problemen oplossen

## Geen reisinformatie

Controleer:

1. `zone.home` bevat geldige latitude- en longitude-waarden.
2. De OpenRouteService API-sleutel is geldig.
3. De wedstrijd heeft geldige coördinaten.
4. Home Assistant heeft toegang tot internet.
5. De HeiGIT/OpenRouteService API is bereikbaar.

---

## Geen wedstrijdgegevens

Controleer de ingestelde KNBSB Team URL.

De URL moet onder andere bevatten:

```text
/clubs/
```

```text
/teams/
```

en:

```text
poolId=
```

---

## Nieuwe configuratieteksten worden niet zichtbaar

Home Assistant kan frontend-vertalingen cachen.

Na het wijzigen van translation-bestanden:

1. Herstart Home Assistant.
2. Voer een harde browser-refresh uit.
3. Test eventueel in een privé/incognitovenster.

---

# Gegevensbronnen

Wedstrijd- en competitiegegevens worden opgehaald uit de publieke diensten die door de KNBSB-website worden gebruikt.

Routegegevens worden berekend met OpenRouteService / HeiGIT.

---

# Privacy

Deze integratie heeft geen eigen externe cloudservice.

De volgende gegevens worden lokaal binnen Home Assistant opgeslagen:

- KNBSB Team URL
- OpenRouteService API-sleutel
- configuratie-instellingen
- route-cache

Wanneer een routeberekening nodig is, worden de volgende gegevens naar OpenRouteService verzonden:

- coördinaten van `zone.home`
- coördinaten van de wedstrijdlocatie

De integratie verstuurt geen Home Assistant gebruikersnaam of wachtwoord.

---

# Beta-status

Huidige versie:

```text
0.1.0-beta.1
```

Dit is een vroege beta-release.

De integratie is tijdens de ontwikkeling getest met een beperkt aantal KNBSB-teams en competities.

Meld onverwacht API-gedrag, ontbrekende wedstrijdgegevens of andere problemen via GitHub Issues.

---

# Geplande functionaliteit

Mogelijke toekomstige uitbreidingen:

- Wedstrijduitslagen
- Afgelopen wedstrijden
- Competitiestand
- Aanvullende wedstrijdstatistieken
- Options Flow voor het achteraf aanpassen van instellingen
- Verdere dashboardintegratie

---

# Ondersteuning en problemen

Problemen kunnen worden gemeld via:

https://github.com/Itchyscratchyback/HA-KNBSB/issues

Vermeld indien mogelijk:

- Home Assistant-versie
- KNBSB-integratieversie
- Relevante foutmelding uit het logboek
- Of het probleem wedstrijddata of reisinformatie betreft

**Plaats nooit je OpenRouteService API-sleutel in een issue.**

---

# Licentie

De broncode wordt beschikbaar gesteld onder de licentie die in het bestand `LICENSE` van deze repository is opgenomen.

---

# Disclaimer

Dit is een onofficieel communityproject.

KNBSB, clubnamen, clublogo's en competitiegegevens kunnen eigendom zijn van hun respectieve rechthebbenden.

Dit project is niet verbonden aan of goedgekeurd door KNBSB, Foys, OpenRouteService of HeiGIT.
