# Sakshub og rik saksdybde

En enkel sak begynner som `saker/<slug>.md`. Huben viser mål, nåstatus, kilder, eier, myndighet, viktige fakta, vurdering, åpne porter og lenke til handling. Den skal være komplett for å vite hvor saken står og hva som må leses videre, ikke bære hele historien.

Når saken vokser, peker huben til `saker/dybde/<slug>/INDEX.md`. Indeksen peker til tema- eller periodefiler og kan peke til nye underindekser. Bruk [dybdemalen](../maler/dybde.md) og [indeksmalen](../maler/indeks.md). Alle detaljer skal kunne nås via hub → rotindeks → underindeks/detalj. En generell søkbar fil er ikke nok hvis leseruten er brutt.

Saksregisteret peker direkte eller via underregistre i `saker/register/` til hver hub. Et område begynner i `areas/<slug>.md` og registreres direkte i `areas/README.md` eller via underregistre i `areas/register/`. Områdets utdyping og historikk legges i `areas/historikk/`, gjerne i en egen temamappe med underindeks. Både områdefilen og `areas/historikk/INDEX.md` skal peke videre til materialet. Bruk denne støttede ruten når et område vokser; egen `areas/dybde/`-struktur inngår ikke i startpakkens kontroller. Historikk i context har tilsvarende egen indeks. Register og indeks er navigasjon; detaljer eies av saken eller fagområdet.

Status, eier, dato for siste oppdatering og kildestatus registreres i hub og dybde. Bruk «utkast» og «uavklart» når grunnlaget mangler. I aktive saker skal faktisk kontrolltid fremgå når ferskhet betyr noe. Separate prosesser med egen myndighet eller ansvar skal ha egne saker og begrunnede krysslenker.

Ved avslutning beholdes en historisk inngang med utfall, dato, sentrale beslutninger og dybdepeker. Fjern uaktuelle aktive prioriteringer. Bevar historiske fakta som historiske, og la originalene ha sitt avtalte hjem.

[Skalering](KONTEKSTSKALERING.md) · [Kilde- og endringsflyt](KONTEKSTFLYT.md)
