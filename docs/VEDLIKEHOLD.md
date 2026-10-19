# Vedlikehold av egen kopi

Behold egne saker, profil, kilder, fullmakter, oppgaver og historikk når startpakken oppdateres. En ny utgave er et grunnlag for sammenligning, ikke noe du skal kopiere blindt over arbeidsmappen.

Ta vare på en versjon eller sikkerhetskopi før endring. Les CHANGELOG og sammenlign først scripts, maler og generelle docs. Avstem nye regler mot egne valg. Kjør verify, tester og en praktisk gjenfinningsprøve etterpå. Ikke flytt data til nye steder bare for å ligne malen.

Grensene eies i config/context-budgets.json. Endring av grenser er en eksplisitt arkitekturbeslutning med begrunnelse og oppdatert dokumenttabell, ikke en måte å få en for stor fil til å passere. Tabellen oppdateres med `python3 scripts/budget.py --write-docs`, og hele kandidaten kontrolleres etterpå.

Oppdaget feil rettes i riktig eier. Relevante forbedringer kan foreslås i det offentlige repoet med oppdiktede eksempler. Ikke ta med egne saker, kontodata eller privat systemhistorikk i et offentlig Issue eller en pull request.
