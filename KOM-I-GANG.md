# Fra nedlasting til første arbeidsøkt

Du kan la et hvilket som helst KI-verktøy med faktisk lesetilgang veilede deg. Be det lese [START-HER-KI.md](START-HER-KI.md) og utføre det det har tilgang til. [KI-veiviseren](docs/KI-OPPSTART.md) dekker også manuell lagring.

## Velg arbeidssted

Bruk en mappe eller et eget privat repo som passer organisasjonens regler. Publisering av malen gir ingen tillatelse til å publisere dine arbeidsdata. En offentlig fork er fortsatt offentlig; bruk ZIP og et separat privat repo for eget arbeid. Behold `.github` og `.gitignore` ved kopiering.

## Fyll inn det nødvendige

I `config/system.json` fyller du `owner`, `original_home` og `delivery_home`. `repository` angir ditt eget `eier/repo` hvis du bruker GitHub. Behold `phase: pilot` og `task_owner: markdown` ved enkel oppstart. Fyll [profil](context/PROFIL.md), [kildekart](context/KILDER.md) og [tilganger](context/TILGANGER.md). Sett `access_confirmed: true` først etter en faktisk lese-, skrive- og gjenfinningsprøve innenfor din fullmakt.

Du kan la uavklarte felt stå som `IKKE_AVKLART` mens du prøver det oppdiktede eksempelet. Dette er en bevisst åpen start, ikke et etablert system for reelle arbeidsdata.

## Koble til samtale eller agent

Et samtaleprosjekt får [CHATGPT-PROSJEKTINSTRUKS.md](CHATGPT-PROSJEKTINSTRUKS.md) som fast peker og tilgang til relevante filer. [CHATGPT-START.md](CHATGPT-START.md) eier den praktiske oppstarten. Dersom prosjektet bare leser vedlegg, lagrer du eller en agent med skrivetilgang endringer tilbake i den autoritative mappen. Bytt ut utdaterte vedlegg bevisst.

En utførende agent leser [AGENTS.md](AGENTS.md). Agenten skal lese gjeldende START og bruke dokumenterte tilganger. Den skal si hvilke filer den faktisk leste. Instruksjonsfilene gir ikke teknisk tilgang eller tillatelse til å sende, publisere eller slette.

## Opprett første sak

Kopier `maler/sak.md` til `saker/din-sak.md`, fyll ut feltene og legg en relativ lenke i `saker/README.md`. Registrer én oppgave med eier, mål, neste handling, frist eller «ingen», og ferdigkriterium i `arbeid/OPPGAVER.md`. Koble saken til oppgaven. Velg første arbeidssteg i `arbeid/UKA.md` uten å kopiere hele oppgaven.

Ved bruk av terminal kan en ny saksfil opprettes slik:

```sh
python3 scripts/new_case.py min-pilot --title "Min første pilotsak"
```

Programmet lager en utkastfil og registerlenke, men finner ikke på eier, frist eller fakta. Fyll ut saken før den gjøres aktiv.

## Godkjenn første pilot

Kjør `python3 scripts/verify.py`. Start en ny økt uten forrige samtale og be: «Les START og finn pilotsaken. Vis mål, faktisk kilde, eier, neste handling og det som fortsatt er uavklart.» Sammenlign med original og lagrede filer. Fyll deretter [oppstartskvitteringen](context/OPPSTART.md) og sett `phase` til `active` først når `--ready` består og den praktiske prøven er gjort.

Valg som trenger mer omtanke er samlet i [avklaringsheftet](opplaering/Avklaringshefte.md). Spørsmål 1–10 er nok til første tilpasning. Full drift krever din egen kontekst, men strukturen og kontrollene er allerede klare.
