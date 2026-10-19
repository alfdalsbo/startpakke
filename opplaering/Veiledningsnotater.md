# Veiledningsnotater til presentasjonen

## 1 Ditt arbeidssystem med KI

Hensikt: Gi en praktisk inngang til et arbeidssystem som kan overtas mellom økter. Forklar at oppsett og tilganger må velges og prøves i deltakerens egen kopi. Full gjennomgang med de to kontrollkapitlene tar omtrent 140 minutter. Bruk øvingsheftets 90-minuttersløp for en kortere økt og velg ut lysbilder etter behov.

## 2 Det du skal kunne

Tid: 3 minutter. Be deltakeren gi et eget eksempel på noe som må forklares på nytt eller lett glipper. Bruk eksempelet som referanse gjennom økten.

## 3 Ansvar i ditt oppsett

Tid: 4 minutter. Verktøyvalget er åpent. Fyll config/system.json i din egen kopi. Start med Markdown-kø eller velg én annen autoritativ kø. ChatGPT-prosjektet er arbeidsflaten, mens tilgang til kilder må testes konkret.

## 4 Systemets deler

Tid: 4 minutter. Følg original til KI, og derfra til kunnskap og oppgave. Pek ut menneskets ansvar for valg og beslutninger. Pilene beskriver arbeidsflyt; hver teknisk forbindelse må faktisk prøves.

## 5 Én eier for hver opplysning

Tid: 4 minutter. Bruk spørsmålet: Hvor skal en endret leveransefrist oppdateres? Riktig svar er i eieroppgaven med grunnlag i originalen. Ukeplanen velger arbeid, men skal ikke bli en parallell oppgaveliste.

## 6 Kontekst som kan vokse

Tid: 3 minutter. START er et rutekart. Saksoversikten gir nødvendig nåstatus og peker videre. Ved omfattende sak brukes indeks og historikk. Originalen kontrolleres når spørsmålet krever det. Første hentebølge er ikke en fast grense.

## 7 Øvelse 1 Sorter innspillet

Tid: 10 minutter. Åpne side 2 i øvingsheftet og les hele innspillet. Be deltakeren skille faktum, hypotese, idé, oppgave og avhengighet. Vis løsningen først etter at deltakeren har forsøkt. Fjordverk er oppdiktet.

## 8 Et innspill får riktig hjem

Tid: 3 minutter som del av gjennomgangen av øvelse 1. En kilde kan gi flere typer innhold. Lagre betydning og peker i saken; en faktisk handling i valgt kø. Bevar beslutningsgrensen. Kontroller lagring og konsekvenser.

## 9 Øvelse 2 En arbeidsklar oppgave

Tid: 10 minutter. Bruk øvingsheftets side 3 og maler/oppgave.md. Forslaget kan være ferdig levert før ledelsen beslutter innføring. En senere effekt skal ikke gjøres til et uklart sluttkriterium for selve notatet.

## 10 Tre datoer med ulik betydning

Tid: 3 minutter. Datoene er et eget illustrasjonseksempel. I Fjordverk-oppgaven er kontrolldato foreløpig ikke avtalt. Ikke dikt en dato for å fylle et felt. Flyttet arbeidsdato betyr ikke at en formell leveransefrist er endret.

## 11 Prioritering innen faktisk kapasitet

Tid: 3 minutter. Forklar prioriteringsregelen i systemmalen. Inntil tre hovedprioriteringer er en øvre ramme, ikke et krav om tre. Reelle frister med vesentlig konsekvens kan overstyre.

## 12 Øvelse 3 Du har 90 minutter

Tid: 15 minutter. Bruk side 4 i øvingsheftet. Et mulig valg er 20 + 45 + 10 minutter og 15 minutter buffer. Notatrydding og nytt kontrollpanel utsettes. Be om begrunnelse, ikke bare en liste. Tidene er øvingsanslag.

## 13 En rytme som holder systemet levende

Tid: 3 minutter. Rytmen er forslag til pilot. Det er nok med kort, nyttig oppfølging. Ukereviewet er historisk; den gjeldende statusen bor fortsatt i sak og oppgave. Ingen rutine er aktivert automatisk.

## 14 Øvelse 4 En nyere kilde endrer fristen

Tid: 15 minutter. Bruk side 5 i øvingsheftet. Senere godkjent e-post flytter leveransefrist til 16. november og bekrefter at fadderordning ikke er besluttet. Arbeidsdatoen 9. november kan beholdes. Spør deretter hva som skal rapporteres hvis saksfilen lagres, men oppgaveoppdateringen feiler.

## 15 Oppstart med ditt KI-verktøy

Tid: 4 minutter. Startmelding: Les START-HER-KI.md og hjelp meg å sette opp systemet. Gjør det du har tilgang til, og veiled meg i resten. KI leser PROJECT, START, oppsett og KI-OPPSTART. Ved bare lesetilgang leverer KI målfil og tekst, eieren lagrer, og ny versjon kontrolleres. Alle oppsett begynner i egen arbeidskopi og med én pilot. Filtilgang er ikke automatisk konto- eller skrivetilgang.

## 16 En presis overlevering

Tid: 3 minutter. Vis maler/oppdrag.md. Oppdragsmappen erstatter ikke den personlige oppgavekøen. En arbeidsordre eller AGENTS.md starter ingen agent av seg selv. Direkte overlevering er en mulig funksjon, ikke et krav for å starte.

## 17 Øvelse 5 En ny økt overtar

Tid: 15 minutter. Bruk side 6 i øvingsheftet. Kontroller konkret hvilket grunnlag assistenten brukte. Hvis testen feiler, rett én rute eller kildepeker og prøv igjen. En troverdig oppsummering er ikke nok.

## 18 Hva som gjør arbeidet ferdig

Tid: 3 minutter. Skille mellom utkast og utsending, fil skrevet i svar og lagret fil, delsteg og hele arbeidsløpet. Menneskelig beslutningsmyndighet gjelder fortsatt. Strukturvalidatoren kontrollerer bare et avgrenset teknisk sett.

## 19 Bytegrenser som holder inngangen kort

Tid: 5 minutter. UTF-8-byte med CRLF normalisert til LF. Varsel og stopp gjelder ved lik eller større størrelse. kB er 1 000 byte. Dashboard er START + CURRENT + PRIORITERINGER. Absolutt tak er 21 600 B for dashboard og 24 000 B for hubruten, men den vanlige kontrollen stopper allerede ved den lavere stoppgrensen. Hver enkelt AGENTS, CHATGPT-START, CURRENT og PRIORITERINGER har i tillegg egne maksimum i config/context-budgets.json. Prosjektinstruksen har 1 500 Unicode-tegn. Dette er lokale designregler, ikke produktgrenser for KI.

## 20 Kontroller før bruk og levering

Tid: 5 minutter. Kjør fra repoets rot med Python 3.10 eller nyere. --ready skal feile før eget oppsett og tilgangstest er registrert. Teknisk kontroll er ikke bevis for at en integrasjon virker eller at innholdet er sant. preflight sjekker den stagede Git-kandidaten mot lest full HEAD-SHA. Ukentlig kontroll: prøv en ny økt, sjekk en kilde og følg én viktig rute.

## 21 Første pilot

Tid: 3 minutter. Tidsplanen er et forslag. Spør hva som vil være en merkbar forbedring etter ti arbeidsdager. Vurder nytte og vedlikehold før flere funksjoner bygges.

## 22 Ditt neste steg

Tid: siste 5 minutter eller egen oppfølging. Be deltakeren peke ut én egnet sak og fylle første del av avklaringsheftet. Resten av de 35 spørsmålene kan tas senere. Bruk tilpasningsprompten når svarene foreligger. Oppgi hva som er produsert, og hva som først kan verifiseres i hans miljø.
