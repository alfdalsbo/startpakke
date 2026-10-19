# Instruks til utførende agent

Ved første oppsett eller uavklart brukeroppsett: følg [START-HER-KI.md](START-HER-KI.md).

Les gjeldende [context/START.md](context/START.md). [PROJECT.md](PROJECT.md) er systemkontrakten; les den ved første oppstart, regelendring og systemarbeid. Kontroller valgt oppsett og faktiske tilganger før bruk av levende data.

Ved konkret arbeid følger du riktig sak eller område, relevant indeks og nødvendig original. Utvid lesingen når grunnlaget ikke er tilstrekkelig. Bevar kildegrad, myndighetsgrenser og nyttige sammenhenger. Ikke last hele basen som standard.

Ved endring følger du [docs/KONTEKSTFLYT.md](docs/KONTEKSTFLYT.md). Vurder alle berørte eiere før skriving, bevar substans ved flytting, og kontroller bytegrenser og leseruter. Kjør `python3 scripts/verify.py` før levering. Ved Git-endringer: stage bare tiltenkte filer, bruk `python3 scripts/preflight.py --expect-head <lest full SHA>` og kontroller samme kandidat før push. Ikke overskriv samtidige endringer.

Når kontrollprogrammer, kontrakter eller budsjettregler endres, kjør også `python3 -m unittest discover -s tests -v`. Bruk [oppdragskøen](oppdrag/README.md) for avgrenset overlevering. Skill oppdragets resultat fra brukerens hovedoppgave.

Utfør autorisert arbeid til ferdigkriteriet er oppfylt. Les tilbake lagrede resultater. Ved delvis feil fortsetter uavhengige deler; rapporter konkret rest og gjenopptakspunkt. Ikke påstå bakgrunnsarbeid uten en faktisk startet mekanisme.

Dette er en offentlig mal. Det skal ikke legges inn reelle personopplysninger, intern arbeidskontekst eller kontodata i distribusjonsrepoet. Egne arbeidsdata tilhører brukerens avklarte kopi. Tillatelser til å lese en kilde gir ikke i seg selv tillatelse til utsending, publisering eller formelle beslutninger.
