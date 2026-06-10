# Fluxuri UI initiale

## 1. Obiectiv

Acest document descrie fluxurile principale de ecran pentru aplicatia web de reconciliere WMS-WME prin ERP.

UI-ul trebuie sa ajute operatorul sa inteleaga evenimentele, regulile aplicate si verdicturile, nu doar totalurile finale.

## 2. Principii UI

1. Evenimentele sunt afisate inaintea totalurilor.
2. REVIEW si NOT_MATCH trebuie sa fie usor de filtrat.
3. Fiecare verdict trebuie sa arate regula aplicata.
4. Orice modificare manuala cere observatie.
5. Importul automat este prezentat ca flux principal.
6. Upload-ul manual este marcat clar ca fallback.

## 3. Dashboard

Scop:

Vedere generala asupra starii sistemului.

Elemente:

- status ultim import WMS;
- status ultim import WME;
- status conexiune ERP;
- produse reconciliate;
- produse in REVIEW;
- produse cu NOT_MATCH;
- erori import;
- rulari recente.

Actiuni:

- porneste import;
- vezi erori;
- deschide reconciliere produs;
- deschide raport final.

## 4. Ecran Importuri

Scop:

Administrarea importurilor automate si manuale.

Sectiuni:

- importuri automate WMS;
- importuri automate WME;
- upload manual fallback;
- log erori;
- campuri lipsa;
- randuri respinse;
- istoric importuri.

Actiuni:

- ruleaza import automat;
- reincarca import esuat;
- descarca log erori;
- incarca fisier manual pentru test.

## 5. Ecran Selectare produs

Scop:

Alegerea produsului, lotului si perioadei pentru reconciliere.

Filtre:

- cod produs;
- denumire produs;
- lot;
- perioada;
- status reconciliere;
- doar REVIEW;
- doar NOT_MATCH.

Actiuni:

- porneste reconciliere;
- vezi istoric rulari;
- vezi evenimente brute WMS;
- vezi evenimente brute WME.

## 6. Ecran Reconciliere produs

Scop:

Ecranul principal de lucru pentru operator.

Sectiuni recomandate:

1. Date produs.
2. Perioada analizata.
3. Opening informativ.
4. Evenimente WMS.
5. Evenimente WME.
6. MATCH.
7. MATCH dupa netare.
8. REVIEW.
9. NOT_MATCH.
10. Totaluri finale.
11. Concluzie.

Regula UI:

Totalurile finale se afiseaza dupa listele de evenimente, nu inainte.

## 7. Ecran Detaliu eveniment

Scop:

Analiza unui eveniment punctual.

Afișeaza:

- eveniment WMS;
- eveniment WME candidat;
- document brut;
- document normalizat;
- data;
- cantitate;
- partener;
- lot;
- regula aplicata;
- verdict propus;
- diferente;
- observatii.

Actiuni:

- confirma MATCH;
- confirma MATCH dupa netare;
- trimite la REVIEW;
- marcheaza NOT_MATCH;
- adauga observatie;
- creeaza match manual cu justificare.

## 8. Ecran Reguli matching

Scop:

Vizualizarea si administrarea regulilor active.

Sectiuni:

- reguli active;
- reguli inactive;
- prioritate reguli;
- descriere regula;
- exemple;
- istoric modificari.

Actiuni:

- activeaza regula;
- dezactiveaza regula;
- testeaza regula pe produs;
- vezi impact estimat.

In MVP, modificarea regulilor poate fi limitata la utilizatori admin.

## 9. Ecran Raport final

Scop:

Generarea raportului de audit.

Raportul include:

- produs;
- lot;
- perioada;
- surse date;
- importuri folosite;
- lista MATCH;
- lista MATCH dupa netare;
- lista REVIEW;
- lista NOT_MATCH;
- totaluri finale;
- concluzie;
- utilizator;
- data generare.

Exporturi estimate:

- PDF;
- DOCX;
- Excel;
- CSV.

## 10. Ecran Administrare

Scop:

Configurarea minima a aplicatiei.

Sectiuni:

- utilizatori;
- roluri;
- permisiuni;
- surse import;
- conexiuni ERP;
- jurnal sistem.

## 11. Roluri utilizator estimate

- Admin;
- Operator reconciliere;
- Reviewer;
- Viewer audit.

## 12. Criterii UX pentru MVP

1. Operatorul trebuie sa poata porni reconcilierea pentru un produs in maximum 3 pasi.
2. REVIEW si NOT_MATCH trebuie sa fie vizibile fara cautare manuala complexa.
3. Regula aplicata trebuie sa fie vizibila pe fiecare match.
4. Upload-ul manual trebuie sa fie etichetat ca fallback.
5. Raportul final trebuie sa poata fi exportat din ecranul de reconciliere.
