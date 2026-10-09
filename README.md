ROADMAP:

| ~~Basis versie met navigatie~~ | -> | ~~Multi-competition versie~~ | -> | Wedstrijd uitslagen toevoegen aan matches| -> | Alle wedstrijd uitslagen per team| -> | Competitie stand | -> | Winkans berekening | -> | Advies aan de hand van Competitie stand punten saldo en vergelijkbare matches | -> 

# KNBSB voor Home Assistant

Een custom Home Assistant-integratie voor KNBSB-competities.

Hoofdpunten van deze integratie:

- Wedstrijdinformatie
- locaties
- kalender integratie
- reisinformatie
-   Afstand in KM
-   Reistijd in minuten
-   Geplande vertrektijd vanaf "zone.home"
-   Geplande aankomst tijd op locatie
-   Instelbare tijd aanwezig voor wedstrijden thuis of uit (wordt meegenomen in vertrektijd)
-   One click Navigatie knop via HA-KNBSB-Card (losse integratie)
-   Navigatie via Android Auto | Apple carplay Homeassistant  Kies: **Navigatie** -> **knbsb_next_match_address**

Voor rijafstand en reistijd wordt OpenRouteService.org gebruikt. Dit is een gratis service waar je kan registreren voor een eigen API key.

> Dit is een onofficiële community-integratie en is niet verbonden aan of goedgekeurd door de KNBSB.

Zie hieronder de view die de integratie ondersteunt samen met de HA-KNBSB-Card integratie

---
### Onderstaande is mogelijk met de HA-KNBSB Schedule card [losse HACS]
<img width="3504" height="1172" alt="screenshot-3" src="https://github.com/user-attachments/assets/7b0201b6-5469-4009-b607-ed334743df44" />


<img width="515" height="694" alt="image" src="https://github.com/user-attachments/assets/c73918ce-8947-4ca7-83d4-c0f5461aa4a9" />

<img width="473" height="609" alt="image" src="https://github.com/user-attachments/assets/ed827cf2-155c-4326-a306-37ea9293fa64" />



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
