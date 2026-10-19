# Fra kilde til kontrollert endring

## Før skriving

Les kilden og eksisterende eier. Avklar hva som er nytt, hvilken sikkerhet opplysningen har og hva den endrer. Finn relevante forbindelser og motstrid. Ikke hopp rett fra ett nytt notat til en oppgave uten å forstå saken.

Beskriv endringssettet: kilde, sak/område, oppgave, prioritering og eventuell fullmakt. Skill lesebredde fra skriveomfang. Du kan trenge å lese bredt uten å endre alle filene. Beregn konsekvensen for filstørrelser og leseruter før publisering, særlig hvis START vokser.

## Samlet kandidat

Oppdater den kanoniske eieren først i arbeidskopien. Flytt detalj og oppdater pekere sammen. Endre bare andre flater som ellers blir feil eller misvisende. Ny fil eller oppgave skal ikke duplisere en eksisterende enhet. Bevar meningsfulle sammenhenger og kildepeker.

Kjør `python3 scripts/verify.py`. Ved Git-arbeid: noter lest HEAD, stage tiltenkte filer og kjør `python3 scripts/preflight.py --expect-head <full SHA>`. Programmet kontrollerer en isolert kopi av hele Git-indeksen og rapporterer tre-ID. Ustaged arbeid er ikke med. Nye endringer i indeksen krever ny kontroll. Push uten force; ved ny ekstern commit må endringen avstemmes og kontrolleres på nytt.

## Etter lagring

Les tilbake faktisk lagret versjon. Kontroller berørt oppgavestatus, frist og prioritering. Verifiser relevant original og semantisk fullføring i tillegg til tekniske kontroller. Hvis en ekstern oppdatering feiler, registrer nøyaktig objekt-ID, tiltenkt endring og restarbeid hos eksisterende eier. Ikke opprett en dublett for å komme rundt feilen.

Kvitter for hva som er ferdig og hva som fortsatt mangler. Lær av tilbakevendende feil ved å rette årsaken og prøve det opprinnelige tilfellet igjen. Ikke legg en ny generell instruks oppå et uklart eierskap.
