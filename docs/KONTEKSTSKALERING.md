# Lesing, bytebudsjetter og vekst

## Progressiv lesing

Begynn med START og den relevante saken eller områdefilen. Følg indeks til nødvendige detaljer og kontroller originalen når ferskhet, formell betydning eller konsekvens krever det. Se også eldre forløp og sideforbindelser som kan endre forståelsen. Flere leseruter kan være nødvendige; et budsjett for normal oppstart er ikke en grense for samlet analyse.

## Maskinelle grenser

[config/context-budgets.json](../config/context-budgets.json) er den maskinelle eieren. Tallene nedenfor genereres fra den, og dokumentkontrollen avviser avvik. Det måles UTF-8-byte etter at CRLF-linjeskift er normalisert til LF. Tegn som æ, ø og å kan bruke flere byte. Tokenanslag brukes ikke som kontrollmål.

| Klasse | Varsel | Blokkering | Absolutt | Regel |
| --- | ---: | ---: | ---: | --- |
| START | 5 400 | 6 000 | – | >= byte |
| START + CURRENT + PRIORITERINGER | 16 000 | 19 000 | 21 600 | >= byte |
| Normal målrettet rute | 19 200 | 21 600 | 24 000 | >= byte |
| Register | 12 000 | 16 000 | – | >= byte |
| Sakshub | 11 000 | 14 000 | – | >= byte |
| Dybde, historikk og manifest | 16 000 | 20 000 | – | >= byte |
| AGENTS.md | – | 6 500 | – | > byte |
| CHATGPT-START.md | – | 10 000 | – | > byte |
| CURRENT alene | – | 12 000 | – | > byte |
| PRIORITERINGER alene | – | 9 000 | – | > byte |
| Fast prosjektinstruks | – | 1 500 | – | > tegn |

Varsel krever vurdering av den berørte ruten. Blokkering krever retting før publisering. Den absolutte grensen viser et ytterligere alvorlig nivå; blokkeringen ved vedlikeholdsgrensen gjelder allerede. START, dashboard, ruter, registre, huber og dybde bruker `>=`; bootstrap- og enkeltfilgrenser fra kontrakten bruker `>` der tabellen angir dette. Prosjektinstruksen måles i Unicode-tegn, ikke byte.

Systemet måler automatisk START + hver toppnivåfil i context, areas og saker, med egen dashboardklasse. Konfigurerte ekstra normalruter måles også. Hver indeks og detaljfil under dybde/historikk/revisjon måles. START + dybde legges ikke automatisk sammen til en universell sesjonsgrense.

Startpakken bruker samme sentrale oppstarts-, dashboard-, rute-, register- og sakshubgrenser som modellen den er utviklet fra. Den har bevisst en enklere, streng regel for historikk: også historiske enkeltfiler har 20 000-bytegrense. Det finnes ingen unntak for e-postledgere eller spesialiserte driftslogger. Å endre status til «historisk» omgår derfor ikke kontrollen. Total samling kan fortsatt vokse ved rekursiv oppdeling.

## Flytt uten å miste kunnskap

1. Finn hva huben må beholde for å gjøre neste økt operativ.
2. Del rik detalj etter framtidige spørsmål, tema eller sammenhengende periode.
3. Flytt materialet til riktig dybdefil; bevar kilder, datoer, begrunnelser, relasjoner og viktig uenighet.
4. Oppdater hub → INDEX → detalj og eventuelle krysslenker i samme kandidat.
5. Ved ren flytting sammenligner du tekstblokker eller hash. Ved omarbeiding vurderer du også semantisk tap. Git-historikk alene erstatter ikke en brukbar leserute.
6. Kjør struktur- og budsjettkontroll og prøv et konkret spørsmål som krever den flyttede detaljen.

En ny e-post eller dato er ikke alene grunn til en fil. Unngå både ubegrenset vekst og oppdeling som skjuler sammenheng. Hvis kjent stoff ofte ikke finnes gjennom registre og målrettet søk, forbedre indeksene før du innfører en ny database.
