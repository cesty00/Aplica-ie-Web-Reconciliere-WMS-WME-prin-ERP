# Aplicație Web Reconciliere WMS-WME prin ERP

Repository pentru dezvoltarea aplicației web de reconciliere între WMS / xTrack și WME / WinMentor prin ERP.

## Scop

Aplicația va funcționa ca strat separat de control, audit, trasabilitate și raportare peste sistemele existente.

- **WMS / xTrack** = sursă operațională pentru mișcări fizice, loturi, locații, recepții, livrări și producție.
- **WME / WinMentor** = sursă ERP/scriptică pentru fișă de magazie, documente economice, gestiuni și stocuri.
- **ERP / integrare automată** = canal principal pentru importul datelor din WMS și WME.
- **Aplicația web** = motor de reconciliere, reguli, matching, audit și export.

**Regula generală:** orice operațiune făcută în WME trebuie să fie făcută și verificabilă în WMS.

## Bază funcțională

Dezvoltarea pornește de la manualul intern de reconciliere WMS-WME, versiune revizuită 17.03.2026.

### Principii principale

1. Reconcilierea se face pe evenimente economice, nu pe totaluri brute.
2. Opening-ul este reper informativ și nu blochează analiza.
3. Totalurile se calculează doar la final.
4. Operațiunile brute se transformă în bucketuri economice comune.
5. Verdicturile sunt **MATCH**, **MATCH după netare**, **REVIEW** și **NOT MATCH**.
6. NOT MATCH se stabilește doar după normalizare, reclasificare, matching și netare.
7. Importul automat prin ERP este fluxul principal; upload-ul manual este fallback.

## Rolurile echipei de dezvoltare

- **Project Manager**: scope, planificare, livrabile, riscuri, Definition of Done.
- **Arhitect Software**: arhitectură, model de date, integrări WinMentor/WMS.
- **Lead Developer**: structură repo, backend, frontend, API, implementare modulară.
- **QA Engineer**: testare, securitate, criterii de acceptanță, Go/No-Go.
- **UI/UX Designer**: fluxuri utilizator, navigație și ecrane operaționale.

## Module estimate

- Import date WMS/WME prin ERP
- Normalizare date
- Canonicalizare operațiuni
- Matching evenimente
- Netare
- Verdict și audit
- Raportare

## MVP inițial

1. Documentație tehnică de bază
2. Model de date inițial
3. Import WMS/WME prin sursă controlată
4. Fallback upload manual
5. Parsare evenimente WMS și WME
6. Canonicalizare operațiuni
7. Matching recepții, livrări și producție
8. Verdicturi MATCH / MATCH după netare / REVIEW / NOT MATCH
9. Ecran reconciliere produs
10. Raport final simplu

## Principiu de siguranță operațională

În MVP, aplicația este **read-only** față de WMS și WME. Ea citește date, reconciliază evenimente și generează rapoarte, dar nu modifică date în sistemele sursă.

## Documentație

După indexarea repository-ului, vor fi create următoarele documente:

- `docs/technical-spec.md` - Specificații tehnice
- `docs/data-model.md` - Modelul de date
- `docs/matching-rules.md` - Reguli de matching
- `docs/ui-flows.md` - Fluxuri utilizator
- `docs/qa-plan.md` - Plan QA și testare
