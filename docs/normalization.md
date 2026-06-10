# Normalizare - MVP-04

## Obiectiv

MVP-04 adauga motorul initial de normalizare pentru evenimente WMS si WME.

Normalizarea pregateste datele pentru canonicalizare si matching, dar nu stabileste verdicturi finale.

## Reguli implementate

- normalizare document;
- normalizare cod produs;
- normalizare lot;
- normalizare partener;
- normalizare cantitate;
- recalcul quantity_signed pentru WME;
- determinare semn economic initial.

## Patternuri speciale detectate

- SFA la inceput de document;
- RET_WME;
- WME<document>-1;
- ANULARE COMANDA.

## Campuri actualizate

Pentru WMS:

- product_code;
- lot_code;
- normalized_document_no;
- partner;
- quantity;
- economic_sign;
- details cu markeri de pattern.

Pentru WME:

- product_code;
- lot_code;
- normalized_document_no;
- partner;
- quantity_in;
- quantity_out;
- quantity_signed;
- stock_after;
- economic_sign.

## Endpointuri

POST /normalization/wms/batches/{import_batch_id}

POST /normalization/wme/batches/{import_batch_id}

## Limite MVP-04

Nu include canonicalizare finala, matching, netare sau verdicturi.
