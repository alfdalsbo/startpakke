# Oppsett og tilgangsprøve

## Enkel mappe

Kopier denne strukturen til godkjent lagring. Fyll ut profil, kildekart og tilgangsmatrise. Velg markdown som oppgaveeier. Gjør START, PROJECT og relevant sak tilgjengelige for KI-arbeidsflaten. Prøv én oppdiktet sak før egne data brukes.

## GitHub

Opprett et privat repositorium i riktig konto. Legg inn hele strukturen, inkludert .github og .gitignore. Kontroller lesbar README og lenker på main. Koble valgt verktøy hvis kontoen støtter det. Test lesing og skriving separat på en øvingsfil. Ikke anta at GitHub-tilkobling gir tilgang til alle repoer eller alle operasjoner.

Ved overgang til Issues: opprett eller finn eier-Issue for hver åpen oppgave i ditt eget repo, behold koblingene, merk tekstkøen historisk og sett task_owner til github_issues. Fyll inn repository som owner/name. Bruk [oppgavemalen](../maler/oppgave.md) og følg [overgangen til GitHub-oppgaver](GITHUB-OPPGAVER.md). Issue-malen i distribusjonsrepoet er for forbedringer av selve startpakken.

## Fem akseptanseprøver

1. Lesing: Assistenten kan finne en kjent opplysning i riktig kilde og oppgi hvilken fil den brukte.
2. Skriving: En autorisert øvingsendring kan finnes igjen på målflaten etter lagring.
3. Overtakelse: En ny økt finner saken, neste handling og åpne spørsmål uten gammel samtale.
4. Motstrid: En nyere kilde fører til korrekt nåstatus og bevart historikk.
5. Fullføring: Ett utført delsteg lukker ikke hele oppgaven når andre ferdigkriterier gjenstår.

Registrer resultat, dato og avgrensning i TILGANGER. Gjenta relevante prøver etter vesentlig endret tilgang eller integrasjon.

## Teknisk kontroll

Python 3.10 eller nyere er bare nødvendig for de valgfrie lokale kontrollene. Ingen ekstra pakker trengs. Kjør `python3 scripts/verify.py` fra rotmappen. På Windows kan du bruke `py -3` i stedet for `python3`. `--ready` krever utfylt eier, originalsted, leveransested, registrert tilgangsavklaring og en bestått [oppstartskvittering](../context/OPPSTART.md) med dato og eksisterende pilotsak. Den urørte malen skal stoppe i denne modusen. En grønn teknisk kontroll erstatter ikke prøvene over. [Kontrolloversikten](KONTROLLER.md) beskriver hele omfanget.

## Senere automatisering

Start med en manuelt utløst flyt. Dokumenter trigger, kildeomfang, fullmakt, resultat, feilmelding og stoppmulighet. Avtal tidsplan først når gjentatte manuelle kjøringer fungerer. Pakken setter ikke opp planlagte arbeidsjobber eller ekstern synk. GitHub Actions kjører filkontroller ved push, pull request og manuell start når Actions er tilgjengelig.
