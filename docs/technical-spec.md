# Specificatie tehnica - Reconciliere WMS-WME prin ERP

## 1. Obiectiv

Aplicatia web reconciliaza operatiunile dintre WMS/xTrack si WME/WinMentor prin ERP.

Aplicatia este un strat separat de control, audit si raportare. Nu inlocuieste WMS, WME sau ERP.

## 2. Regula generala

Orice operatiune facuta in WME trebuie sa fie disponibila si verificabila logic in WMS.

Reconcilierea se face pe evenimente economice, nu prin egalizarea fortata a totalurilor brute.

## 3. Sisteme sursa

- WMS/xTrack: miscari fizice, loturi, locatii, receptii, livrari, productie.
- WME/WinMentor: fisa de magazie, documente economice, gestiuni, stocuri scriptice.
- ERP: canal principal de import automat.
- Aplicatia web: reconciliere, reguli, audit, export.

## 4. Principii functionale

1. Opening-ul este informativ si nu blocheaza analiza.
2. Totalurile se calculeaza doar la final.
3. Semnul economic are prioritate fata de eticheta bruta.
4. Operatiunile brute se transforma in bucketuri economice comune.
5. NOT MATCH se stabileste doar dupa normalizare, reclasificare, matching si netare.
6. Importul automat prin ERP este fluxul principal.
7. Upload-ul manual este fallback pentru testare sau audit punctual.

## 5. Module principale

### 5.1 Import date

Responsabilitati:

- import automat date WMS prin ERP;
- import automat date WME prin ERP;
- fallback upload manual;
- jurnalizare importuri;
- validare campuri obligatorii;
- raportare erori import.

### 5.2 Normalizare date

Responsabilitati:

- normalizare cod produs;
- normalizare lot;
- normalizare document;
- normalizare partener;
- normalizare data;
- normalizare cantitate;
- determinare semn economic.

### 5.3 Canonicalizare operatiuni

Transforma operatiunile brute in bucketuri economice comune:

- Receipt;
- Delivery;
- Return;
- Transfer;
- Consum productie;
- Predare produs finit;
- Ajustare;
- Review.

### 5.4 Matching evenimente

Compara evenimente WMS si WME dupa:

- document;
- document normalizat;
- data;
- cantitate;
- partener;
- lot;
- comanda productie;
- sens economic;
- context operational.

### 5.5 Netare

Aplica reguli de netare pentru evenimente care nu bat brut, dar pot bate economic dupa agregare sau anulare/revers.

### 5.6 Verdict si audit

Verdicturi acceptate:

- MATCH;
- MATCH dupa netare;
- REVIEW;
- NOT MATCH.

Fiecare verdict trebuie sa pastreze regula aplicata si sursele folosite.

### 5.7 Raportare

Rapoarte estimate:

- raport produs;
- raport lot;
- raport perioada;
- export audit;
- lista REVIEW;
- lista NOT MATCH.

## 6. MVP

MVP-ul va include:

1. documentatie tehnica;
2. model de date initial;
3. import WMS/WME din surse controlate;
4. fallback upload manual;
5. parsare evenimente;
6. canonicalizare;
7. matching pentru receptii, livrari si productie;
8. verdicturi de baza;
9. ecran reconciliere produs;
10. raport final simplu.

## 7. Limite MVP

In MVP, aplicatia este read-only fata de WMS si WME.

Nu modifica date in sistemele sursa.

Functiile de scriere inapoi in ERP/WMS/WME sunt excluse din MVP si necesita aprobare separata.
