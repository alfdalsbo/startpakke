# Et arbeidssystem med KI

En norsk startpakke for å gjøre arbeid kumulativt: Bevar forståelse og kilder, velg konkrete neste handlinger og la en ny økt fortsette der den forrige slapp. Du får en ferdig mappestruktur, regler for hvordan KI leser og oppdaterer den, maler, eksempler og kontroller for vekst og gjenfinning.

## La KI hjelpe deg i gang

Gi KI-verktøyet tilgang til mappen og be: **«Les START-HER-KI.md og hjelp meg å sette opp systemet. Gjør det du har tilgang til, og veiled meg i resten.»** [KI-inngangen](START-HER-KI.md) forklarer oppsettet både for verktøy med skrivetilgang og for samtaler der du lagrer manuelt. Ingen tidligere kontekst er nødvendig.

## Kom i gang

1. Velg **Code → Download ZIP**, pakk ut og legg filene i en mappe du har lov til å bruke. Vil du bruke GitHub, opprett et **eget privat repositorium** og legg inn filene der. Behold mappestrukturen. Dette offentlige repoet er en distribusjonsmal; egne arbeidsdata hører hjemme i din egen godkjente kopi.
2. Åpne [KOM-I-GANG.md](KOM-I-GANG.md). Fyll inn eier, kildeplassering og leveransested i [config/system.json](config/system.json), og beskriv rollen din i [profilen](context/PROFIL.md). Velg én oppgavekø.
3. Gjør filene tilgjengelige for din KI-arbeidsflate. For et samtaleprosjekt bruker du [den korte prosjektinstruksen](CHATGPT-PROSJEKTINSTRUKS.md). En kodeagent bruker [AGENTS.md](AGENTS.md). Kontroller faktisk lesing og skriving; en opplastet fil gir ikke automatisk tilgang til resten.
4. Prøv [eksempelet](eksempler/README.md), opprett én egen sak fra [saksmalen](maler/sak.md), og legg én handling i [oppgavekøen](arbeid/OPPGAVER.md).
5. Start en ny økt. Be den finne målet, kilden, eieren og neste handling. Deretter bruker du systemet i ti arbeidsdager før du utvider.

Du trenger ikke programmere for å bruke tekstfilene. Markdown-filer (`.md`) er vanlig tekst med enkel formatering. Python 3.10 eller nyere trengs bare for kontrollprogrammene; de bruker standardbiblioteket og trenger ingen pakkeinstallasjon.

## Prøv kontrollen

Kjør fra rotmappen:

```sh
python3 scripts/verify.py
python3 scripts/budget.py
python3 scripts/verify.py --ready
python3 -m unittest discover -s tests -v
```

På Windows kan du bruke `py -3` i stedet for `python3`. Vanlig kontroll skal bestå på den urørte malen. `--ready` skal feile inntil grunnoppsettet og en reell pilot er på plass. Den kontrollerer registrerte opplysninger, ikke om eksterne tilganger faktisk virker. Bruk [tilgangsprøven](docs/OPPSETT.md).

## Systemets eiere

| Sted | Ansvar |
| --- | --- |
| [PROJECT.md](PROJECT.md) | Felles kontrakt og arbeidsprinsipper |
| [context/START.md](context/START.md) | Kort leserute, ikke et saksarkiv |
| [context](context/README.md) | Profil, kilder, nåstatus og prioriteringer |
| [saker](saker/README.md) og [areas](areas/README.md) | Konkret saksforståelse og varige ansvarsområder |
| [arbeid](arbeid/README.md) | Én oppgavekø, valgt uke og historiske reviewer |
| [oppdrag](oppdrag/README.md) | Avgrensede arbeidsordrer til en utførende agent |
| [docs](docs/README.md) | Lesing, eierskap, vekst, endring og fullføring |
| [maler](maler/README.md) og [prompts](prompts/README.md) | Kopierbare utgangspunkt og ferdige bestillinger |
| [opplaering](opplaering/README.md) | Håndbok, øvelser, spørsmål og illustrasjoner |

## Når systemet vokser

START varsler ved 5 400 UTF-8-byte og blokkerer ved 6 000. En normal målrettet rute varsler ved 19 200 og blokkerer ved 21 600. En sakshub varsler ved 11 000 og blokkerer ved 14 000. Hele tabellen står i [bytebudsjettene](docs/KONTEKSTSKALERING.md) og eies maskinelt av [konfigurasjonen](config/context-budgets.json).

Flytt rik detalj til sammenhengende tema- eller historikkfiler, oppdater indeksene og kontroller at innholdet fortsatt kan finnes. Grenser beskytter leserutene; de er aldri grunn til å slette relevant kunnskap eller avslutte undersøkelsen for tidlig.

## Hva som følger med

Ingen kontoer, bakgrunnsjobber eller eksterne integrasjoner aktiveres. GitHub Actions kontrollerer repoets filer ved push, pull request og manuell kjøring når Actions er tilgjengelig. Kontrollen bruker ingen hemmeligheter eller skrivetilgang. Se [kontrollomfang](docs/KONTROLLER.md), [endringer](CHANGELOG.md), [bidrag](CONTRIBUTING.md) og [lisens](LICENSE).
