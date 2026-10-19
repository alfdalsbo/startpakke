# Hva kontrollene gjør

Alle programmer er lokale og bruker Python-standardbiblioteket. Kontrollkommandoene leser filer; `new_case.py` oppretter en sak og registerlenke, og `budget.py --write-docs` oppdaterer den dokumenterte budsjetttabellen. Programmene gir ikke tilgang til eksterne systemer.

| Kommando | Kontrollerer |
| --- | --- |
| `python3 scripts/verify.py` | Nødvendige filer, konfigurasjon, én oppgaveeier, datoer, metadata, lenker, register- og dybderuter, bytegrenser og åpenbare hemmeligheter |
| `python3 scripts/budget.py` | Samme budsjettregler, med størrelse og klasse for hver målt fil/rute |
| `python3 scripts/verify.py --ready` | I tillegg utfylt grunnoppsett, pilotlenke og registrert bestått oppstart |
| `python3 scripts/verify.py --public` | I tillegg at distribusjonsmalen har urørt oppstartskonfigurasjon, tom personlig oppgavekø og ingen egne saker |
| `python3 scripts/preflight.py --expect-head <SHA>` | Hele staged Git-kandidaten i en isolert kopi, bundet til lest HEAD og rapportert tre-ID |
| `python3 -m unittest discover -s tests -v` | Regresjoner for grenser, lenker, eierskap, metadata, nåbarhet og kandidatkontroll |
| `python3 scripts/new_case.py <slug> --title "Tittel"` | Oppretter utkast og registerlenke, nekter overskriving |

`--json` finnes på verify, budget og preflight for maskinlesbar rapport. Et vellykket preflight betyr kontrollert struktur på angitt tre, ikke godkjent original, eksterne tilganger eller innholdets semantiske kvalitet. Etter commit sammenlignes commitens tre med den kontrollerte tre-ID-en.

GitHub Actions kjører full verify og tester ved push, pull request og manuell start. Ingen planlagt jobb eller ekstern synk inngår. Kontrollen trenger bare lesetilgang. Actions på en gammel SHA eller en hoppet over kjøring er ikke bevis for ny kandidat.

Lenkekontrollen sjekker at lokale mål finnes og at registrerte saks- og dybderuter kan følges. Den kontrollerer ikke interne `#ankere` mot overskrifter eller om eksterne nettlenker virker og viser riktig kilde. Prøv disse separat når de er viktige for leseruten.

Hemmelighetskontrollen fanger et avgrenset sett tydelige mønstre og filtyper. Den kan ikke garantere at en publisering er fri for personopplysninger, taushetsbelagt informasjon eller alle typer nøkler. Ved offentlig bidrag brukes også menneskelig/agentbasert innholdskontroll. Fullmakter og verifisert original er fortsatt eget ansvar.
