# Arkitektur

En samtale er et arbeidsrom. Varige filer og én oppgavekø gjør arbeidet mulig å overta mellom økter. Originalkildene beholder sin autoritet; repoet gjør betydning, sammenheng og neste handling gjenfinnbar.

| Lag | Eier | Leses når |
| --- | --- | --- |
| Kontrakt | PROJECT og fagregler i docs | Første økt, endring og arbeid som berører regelen |
| Ruting | context/START | Normal oppstart |
| Arbeidsoversikt | CURRENT, PRIORITERINGER, UKA | Status, prioritering og planlegging |
| Saksforståelse | saker og areas | Relevant sak/fagområde |
| Rik detalj | saker/dybde og historikk | Spørsmålet trenger bakgrunn, evidens eller presedens |
| Handling | Én valgt oppgavekø | Neste steg, ansvar og frist |
| Utførelse | oppdrag | En avgrenset agentoverlevering |
| Original | Registrert dokument-/fagsystem | Ferskhet, formell betydning eller kildekontroll |

En viktig sammenheng beskrives der den trengs: hva bygger på, endrer, motsier eller avhenger av hva? Krysslenker har begrunnelse; samme historie vedlikeholdes ikke flere steder. Nye funksjoner innføres når et dokumentert behov ikke løses godt av eksisterende struktur.

Kapasitet måles på varm start, målrettede ruter, registre, huber og hver detaljfil. Total kunnskapsmengde har ikke et samlet tak. Dette er et filbasert arbeidssystem, ikke en ferdig integrasjonsplattform. [Skalering](KONTEKSTSKALERING.md) og [eiere](KONTEKSTEIERSKAP.md) gjør det mulig å vokse uten bred lasting ved hver oppstart.
