# Import WME - MVP-03

## Obiectiv

MVP-03 adauga importul initial WME pentru fisa de magazie / WinMentor.

Importul este read-only fata de WME. Datele sunt salvate doar in baza aplicatiei.

## Regula de proiect

Fluxul principal ramane importul automat prin ERP.

Upload-ul manual WME este fallback pentru testare, audit punctual si situatii exceptionale.

## Formate acceptate

- CSV
- XLSX
- XLS

## Campuri obligatorii

- product_code
- event_date
- document_type
- document_no

Este obligatorie cel putin una dintre coloanele de cantitate:

- quantity_in
- quantity_out

## Calcul quantity_signed

quantity_signed se calculeaza astfel:

quantity_signed = quantity_in - quantity_out

Exemple:

- intrare 10 si iesire 0 => quantity_signed = 10
- intrare 0 si iesire 10 => quantity_signed = -10

## Persistare

Randurile valide sunt mapate in tabela wme_events.

In MVP-03 nu se calculeaza final normalized_document_no, canonical_bucket sau economic_sign. Acestea sunt pentru MVP-04 si MVP-05.

## Status import

- SUCCESS: toate randurile sunt valide.
- PARTIAL_SUCCESS: exista randuri valide si randuri respinse.
- FAILED: nu exista randuri valide.

## Endpoint fallback manual

POST /imports/wme/manual

Raspunsul include import_batch_id, source_system, import_type, status, records_imported, records_rejected si error_log.

## Limite MVP-03

Nu include import automat ERP real, normalizare documente, canonicalizare, matching, netare sau verdicturi.
