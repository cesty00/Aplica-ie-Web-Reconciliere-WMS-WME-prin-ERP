# Plan MVP - Aplicație Web Reconciliere WMS-WME prin ERP

## 1. Obiectiv

Acest document transformă documentația inițială într-un plan de implementare MVP.

MVP-ul trebuie să demonstreze fluxul principal: import date WMS/WME, normalizare, canonicalizare, matching, netare, verdict și raportare.

## 2. Reguli de bază MVP

1. Aplicația este read-only față de WMS și WME.
2. Importul automat prin ERP este fluxul principal.
3. Upload-ul manual este fallback pentru testare și audit punctual.
4. Reconcilierea se face pe evenimente economice, nu pe totaluri brute.
5. NOT_MATCH este permis doar după normalizare, reclasificare, matching și netare.
6. Orice modificare manuală de verdict cere observație.
7. Totalurile se afișează doar după clasificarea evenimentelor.

## 3. Stack tehnic recomandat

### Backend

- Python
- FastAPI
- SQLAlchemy sau SQLModel
- Alembic pentru migrări
- Pydantic pentru validare date

### Frontend

- React
- TypeScript
- Vite
- UI components simple și auditabile

### Database

- PostgreSQL

### Procesare date

- pandas
- openpyxl
- validări custom pe câmpuri obligatorii

### Rapoarte

- Excel
- PDF
- DOCX, ulterior dacă este necesar

### Infrastructură

- Docker
- Docker Compose pentru mediu local
- GitHub Actions pentru verificări minime

## 4. Etape MVP

## MVP-00 - Project setup and repository structure

Scop:

Pregătirea structurii tehnice de bază.

Livrabile:

- structură backend;
- structură frontend;
- structură docs;
- configurare Docker minimă;
- configurare testare minimă;
- README actualizat cu instrucțiuni locale.

Definition of Done:

- proiectul poate fi clonat;
- backend-ul poate porni local;
- frontend-ul poate porni local;
- există comandă clară de test;
- nu există integrare live cu WMS/WME în această etapă.

## MVP-01 - Define database schema

Scop:

Implementarea modelului de date inițial.

Livrabile:

- products;
- lots;
- import_batches;
- wms_events;
- wme_events;
- reconciliation_runs;
- reconciliation_matches;
- audit_logs.

Definition of Done:

- schema este migrabilă;
- relațiile principale sunt definite;
- datele brute și datele normalizate pot fi păstrate separat;
- verdicturile au câmp pentru regula aplicată.

## MVP-02 - Implement WMS import model

Scop:

Pregătirea importului WMS din sursă controlată.

Livrabile:

- parser WMS;
- validare câmpuri obligatorii;
- mapare către wms_events;
- log erori import;
- suport fallback upload manual.

Definition of Done:

- un fișier/sursă WMS controlată poate fi importată;
- rândurile invalide sunt raportate;
- datele brute sunt păstrate;
- importul nu modifică sistemul sursă.

## MVP-03 - Implement WME import model

Scop:

Pregătirea importului WME din fișa de magazie / ERP.

Livrabile:

- parser WME;
- validare câmpuri obligatorii;
- mapare către wme_events;
- calcul quantity_signed;
- log erori import.

Definition of Done:

- o fișă WME controlată poate fi importată;
- intrările și ieșirile sunt citite cu semn economic;
- datele brute sunt păstrate;
- importul nu modifică sistemul sursă.

## MVP-04 - Implement normalization engine

Scop:

Normalizarea datelor înainte de matching.

Livrabile:

- normalizare documente;
- normalizare cod produs;
- normalizare lot;
- normalizare partener;
- normalizare cantități;
- normalizare dată;
- determinare semn economic.

Definition of Done:

- documentele cu prefix SFA pot fi normalizate;
- patternurile RET_WME și WME<doc>-1 sunt detectate;
- ANULARE COMANDA este detectată ca revers posibil;
- normalizarea nu șterge valoarea brută.

## MVP-05 - Implement canonical bucket engine

Scop:

Transformarea operațiunilor brute în bucketuri economice.

Livrabile:

- RECEIPT;
- DELIVERY;
- RETURN_IN;
- TRANSFER;
- TRANSFER_3P;
- PRODUCTION_CONSUMPTION;
- FINISHED_GOOD_OUTPUT;
- ADJUSTMENT;
- REVIEW.

Definition of Done:

- fiecare eveniment primește bucket economic sau REVIEW;
- regulile sunt testabile;
- eticheta brută nu este folosită singură pentru verdict final.

## MVP-06 - Implement matching engine v1

Scop:

Primul motor de matching pe evenimente.

Livrabile:

- matching recepții;
- matching livrări;
- matching retururi simple;
- matching BC cu PRODUCTION-IN;
- matching NP cu PRODUCTION-OUT;
- suport MATCH_AFTER_NETTING;
- REVIEW pentru cazuri neclare;
- NOT_MATCH doar după reguli obligatorii.

Definition of Done:

- evenimentele sunt clasificate reproductibil;
- regula aplicată este salvată;
- diferențele de cantitate sunt calculate;
- NOT_MATCH nu apare prematur.

## MVP-07 - Implement reconciliation run API

Scop:

API pentru rularea reconcilierii pe produs/lot/perioadă.

Livrabile:

- endpoint creare rulare reconciliere;
- endpoint status rulare;
- endpoint rezultate MATCH;
- endpoint rezultate REVIEW;
- endpoint rezultate NOT_MATCH;
- endpoint detaliu eveniment.

Definition of Done:

- reconcilierea poate fi pornită pentru un produs;
- rezultatele pot fi citite prin API;
- statusul rulării este clar;
- erorile sunt raportate.

## MVP-08 - Implement dashboard UI

Scop:

Primul ecran operațional.

Livrabile:

- status importuri;
- produse cu REVIEW;
- produse cu NOT_MATCH;
- rulari recente;
- acces către ecranul de reconciliere.

Definition of Done:

- operatorul vede rapid starea sistemului;
- REVIEW și NOT_MATCH sunt vizibile;
- dashboard-ul nu ascunde erorile de import.

## MVP-09 - Implement product reconciliation UI

Scop:

Ecranul principal de lucru pentru reconciliere.

Livrabile:

- selectare produs;
- selectare lot/perioadă;
- afișare evenimente WMS;
- afișare evenimente WME;
- liste MATCH;
- liste MATCH_AFTER_NETTING;
- liste REVIEW;
- liste NOT_MATCH;
- totaluri finale după evenimente.

Definition of Done:

- operatorul poate urmări verdictul fiecărui eveniment;
- regula aplicată este vizibilă;
- totalurile apar după clasificare;
- modificarea manuală cere observație.

## MVP-10 - Implement QA fixtures and acceptance tests

Scop:

Validarea MVP pe seturi de date controlate.

Livrabile:

- fixture WMS simplu;
- fixture WME simplu;
- caz recepție MATCH;
- caz livrare MATCH;
- caz producție MATCH;
- caz MATCH_AFTER_NETTING;
- caz REVIEW;
- caz NOT_MATCH real;
- teste pentru blocarea NOT_MATCH prematur.

Definition of Done:

- testele rulează local;
- cazurile principale sunt acoperite;
- verdicturile sunt explicabile;
- QA poate da GO/NO-GO.

## 5. Ordinea recomandată de execuție

1. MVP-00
2. MVP-01
3. MVP-02
4. MVP-03
5. MVP-04
6. MVP-05
7. MVP-06
8. MVP-07
9. MVP-08
10. MVP-09
11. MVP-10

## 6. Criteriu general de finalizare MVP

MVP-ul este acceptat doar dacă poate importa date controlate WMS/WME, poate reconcilia evenimente economice de bază, poate produce verdicturi auditabile și poate genera un raport simplu fără să modifice date în WMS sau WME.
