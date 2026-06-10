# Reguli de matching WMS-WME

## 1. Obiectiv

Acest document defineste regulile initiale de matching intre evenimentele WMS si WME.

Matching-ul se face pe evenimente economice. Totalurile sunt calculate doar dupa clasificarea evenimentelor.

## 2. Verdicturi

Verdicturi acceptate:

- MATCH
- MATCH_AFTER_NETTING
- REVIEW
- NOT_MATCH

NOT_MATCH se aplica doar dupa normalizare, reclasificare si netare.

## 3. Bucketuri economice

Bucketuri principale:

- RECEIPT
- DELIVERY
- RETURN_IN
- TRANSFER
- TRANSFER_3P
- PRODUCTION_CONSUMPTION
- FINISHED_GOOD_OUTPUT
- ADJUSTMENT
- DELIVERY_REVERSAL
- REGULARIZATION
- REVIEW

## 4. Normalizare documente

### 4.1 Prefixe livrare

Documentele WMS de tip livrare pot contine prefixe precum SFA.

Exemplu:

- SFA45585 devine 45585

Regula se aplica inainte de matching cu documentul WME.

### 4.2 Retururi WMS

Patternuri tratate ca retur:

- RET_WME...
- WME<document>-1

Acestea se trateaza ca RETURN_IN, nu ca receptie furnizor standard.

### 4.3 Transferuri

Comenzile WMS care incep cu TRANSFER_ pot reprezenta livrari catre terti.

Locatii relevante:

- VER100
- LIV100

Parteneri 3P cunoscuti:

- KYO
- AMBALARE GENERAL AGROCOM

## 5. Receptii

Candidati:

- WMS Receptie pozitiva
- WME FE pozitiv
- WME AE pozitiv ca inbound candidate

Cheie principala:

- document + data + cantitate

Fallback:

- partener + lot + cantitate

Observatie:

Pentru anumite produse finite, WMS Receptie poate reprezenta predare de produs finit si poate avea corespondent WME NP.

## 6. Livrari

Candidati:

- WMS Livrare negativa
- WME AE negativ

Cheie principala:

- document normalizat + cantitate

Fallback:

- partener + data +/- 1 zi + cantitate

Observatie:

Livrarea pozitiva WMS nu se trateaza automat ca retur. Ea intra initial in DELIVERY_REVERSAL sau REVIEW.

## 7. Return-uri

Candidati:

- WMS RET_WME...
- WMS WME<document>-1
- WME AE pozitiv
- alte intrari reclasificate justificat

Cheie principala:

- document de baza + cod produs

Fallback:

- document normalizat + cantitate

## 8. Productie - consum

Candidati:

- WMS PRODUCTION-IN
- WME BC

Cheie principala:

- comanda productie + cantitate

Fallback:

- data + cod produs + cantitate
- netare pe eveniment

## 9. Productie - predare produs finit

Candidati:

- WMS PRODUCTION-OUT
- WME NP

Cheie principala:

- document productie + cantitate

Fallback:

- comanda productie + data + cantitate
- netare pe eveniment

## 10. Transferuri productie

Un eveniment WMS poate corespunde in WME unui lant de documente:

- NT iesire 3711
- NT intrare 301
- BC consum productie

Matching-ul se face pe eveniment economic, nu neaparat pe document unic.

## 11. Ajustari

Ajustarile nu intra automat la NOT_MATCH.

Reguli:

- COR STOC se verifica in context.
- ANULARE COMANDA se trateaza ca revers de livrare.
- Ajustarile pot explica un consum, output sau corectie zilnica.

Doar ajustarile ramase neexplicate dupa netare pot deveni NOT_MATCH.

## 12. Netare obligatorie

Se neteaza obligatoriu:

1. documentele F;
2. evenimente WMS mixte din aceeasi zi / acelasi document;
3. Ajustare pozitiva cu motiv ANULARE COMANDA impreuna cu livrarea de baza;
4. fluxurile TRANSFER_CG... pe comanda;
5. evenimentele de productie unde liniile brute nu bat, dar evenimentul economic poate bate net.

## 13. Ordine de procesare

1. Extrage evenimente WMS pentru produs/lot/perioada.
2. Extrage evenimente WME pentru produs/lot/perioada.
3. Normalizeaza documente, parteneri, loturi si cantitati.
4. Canonicalizeaza operatiunile.
5. Aplica regulile speciale.
6. Construieste MATCH.
7. Construieste MATCH_AFTER_NETTING.
8. Construieste REVIEW.
9. Construieste NOT_MATCH.
10. Calculeaza totalurile finale.

## 14. Regula de siguranta

Aplicatia nu trebuie sa produca verdict final NOT_MATCH pentru un eveniment inainte ca regulile de normalizare, reclasificare si netare sa fie aplicate.
