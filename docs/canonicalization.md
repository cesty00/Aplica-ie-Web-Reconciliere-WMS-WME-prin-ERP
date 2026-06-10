# Canonicalizare - MVP-05

## Obiectiv

MVP-05 transforma operatiunile brute WMS/WME in bucketuri economice comune.

Canonicalizarea pregateste datele pentru matching, dar nu stabileste verdicturi finale.

## Bucketuri implementate

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

## Reguli WMS initiale

- receptie -> RECEIPT
- livrare sau semn negativ -> DELIVERY
- RET_WME sau WME<doc>-1 -> RETURN_IN
- ANULARE COMANDA -> DELIVERY_REVERSAL
- transfer -> TRANSFER
- transfer catre VER100/LIV100 -> TRANSFER_3P
- PRODUCTION-IN / consum -> PRODUCTION_CONSUMPTION
- PRODUCTION-OUT / predare -> FINISHED_GOOD_OUTPUT
- corectie stoc / ajustare -> ADJUSTMENT
- neclar -> REVIEW

## Reguli WME initiale

- FE/NIR pozitiv -> RECEIPT
- AE negativ -> DELIVERY
- AE pozitiv -> RETURN_IN
- BC -> PRODUCTION_CONSUMPTION
- NP -> FINISHED_GOOD_OUTPUT
- NT -> TRANSFER
- PV/COR/REG -> ADJUSTMENT
- neclar -> REVIEW

## Endpointuri

POST /canonicalization/wms/batches/{import_batch_id}

POST /canonicalization/wme/batches/{import_batch_id}

## Limite MVP-05

Nu include matching, netare sau verdicturi MATCH/NOT_MATCH.
