# Plan QA initial

## 1. Obiectiv

Acest document defineste planul initial de testare pentru aplicatia de reconciliere WMS-WME prin ERP.

Scopul QA este sa previna concluziile incorecte, in special verdicturile NOT_MATCH date prea devreme.

## 2. Principii QA

1. Aplicatia trebuie sa respecte manualul de reconciliere WMS-WME.
2. Reconcilierea se testeaza pe evenimente economice, nu doar pe totaluri.
3. NOT_MATCH este permis doar dupa normalizare, reclasificare, matching si netare.
4. Importul automat prin ERP este flux principal.
5. Upload-ul manual este fallback.
6. MVP-ul este read-only fata de WMS si WME.

## 3. Tipuri de testare

### 3.1 Testare import

Se verifica:

- import WMS;
- import WME;
- import nomenclator;
- campuri obligatorii;
- randuri respinse;
- log erori;
- reluare import esuat;
- diferenta intre import automat si upload manual.

### 3.2 Testare normalizare

Se verifica:

- cod produs;
- lot;
- document;
- data;
- cantitate;
- partener;
- semn economic.

Cazuri obligatorii:

- SFA45585 -> 45585;
- RET_WME ca retur;
- WME<document>-1 ca retur;
- TRANSFER_ ca potential flux 3P;
- ANULARE COMANDA ca revers de livrare.

### 3.3 Testare canonicalizare

Se verifica incadrarea in bucketuri:

- RECEIPT;
- DELIVERY;
- RETURN_IN;
- TRANSFER;
- TRANSFER_3P;
- PRODUCTION_CONSUMPTION;
- FINISHED_GOOD_OUTPUT;
- ADJUSTMENT;
- REVIEW.

### 3.4 Testare matching

Se verifica matching pentru:

- receptii;
- livrari;
- retururi;
- consum productie;
- predare produs finit;
- transferuri 3P;
- transferuri productie;
- ajustari.

### 3.5 Testare netare

Se verifica:

- documente F;
- reversuri de livrare;
- ANULARE COMANDA;
- evenimente WMS mixte;
- TRANSFER_CG;
- lant NT -> NT -> BC.

### 3.6 Testare UI

Se verifica:

- dashboard;
- ecran importuri;
- ecran selectare produs;
- ecran reconciliere produs;
- ecran detaliu eveniment;
- ecran reguli matching;
- raport final.

### 3.7 Testare audit

Se verifica:

- pastrarea sursei;
- pastrarea randului sursa;
- regula aplicata;
- utilizatorul care modifica verdictul;
- observatia obligatorie la modificari manuale;
- exportul raportului.

### 3.8 Testare securitate

Se verifica:

- autentificare;
- roluri;
- permisiuni;
- limitarea accesului la administrare;
- protectie fisiere upload;
- log actiuni utilizator.

## 4. Criterii de acceptanta MVP

MVP-ul este acceptabil daca:

1. poate importa seturi WMS si WME controlate;
2. pastreaza datele brute si datele normalizate;
3. canonicalizeaza operatiunile principale;
4. genereaza verdicturi MATCH, MATCH_AFTER_NETTING, REVIEW si NOT_MATCH;
5. nu genereaza NOT_MATCH inainte de aplicarea regulilor obligatorii;
6. permite revizie manuala cu observatie;
7. genereaza raport final simplu;
8. nu scrie date inapoi in WMS sau WME;
9. are audit trail minim.

## 5. Criterii Go/No-Go

### GO

Se poate continua daca:

- importurile functioneaza pe date controlate;
- regulile principale dau rezultate reproductibile;
- REVIEW si NOT_MATCH sunt explicabile;
- raportul final include sursele si regulile aplicate;
- nu exista scriere in sistemele sursa.

### NO-GO

Nu se promoveaza daca:

- lipsesc campuri obligatorii fara blocare clara;
- NOT_MATCH apare fara normalizare si netare;
- datele brute sunt pierdute;
- operatorul poate modifica verdict fara observatie;
- aplicatia scrie in WMS/WME fara aprobare explicita;
- raportul nu permite auditarea sursei.

## 6. Produse test recomandate

Seturile de test trebuie sa includa produse:

- simple, cu receptii si livrari clare;
- cu productie;
- cu retururi;
- cu transferuri 3P;
- cu ajustari;
- cu cazuri de netare;
- cu diferente reale controlate.

## 7. Definition of Done QA

Un livrabil trece QA daca:

- are criterii de acceptanta;
- are cazuri de test;
- rezultatul este reproductibil;
- erorile sunt documentate;
- verdicturile sunt explicabile;
- comportamentul respecta manualul de reconciliere.
