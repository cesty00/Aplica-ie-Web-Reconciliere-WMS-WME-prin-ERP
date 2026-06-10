# Import WMS - MVP-02

## Obiectiv

MVP-02 adauga importul initial WMS pentru aplicatia de reconciliere WMS-WME prin ERP.

Importul este read-only fata de WMS. Datele sunt salvate doar in baza aplicatiei.

## Regula de proiect

Fluxul principal ramane importul automat prin ERP.

Upload-ul manual WMS este fallback pentru testare, audit punctual si situatii exceptionale.

## Formate acceptate

- CSV
- XLSX
- XLS

## Campuri obligatorii

- product_code
- event_date
- raw_operation_type
- quantity

Daca lipseste o coloana obligatorie, importul returneaza eroare.

Daca un rand are valori invalide, randul este respins si eroarea se salveaza in error_log.

## Persistare

Randurile valide sunt mapate in tabela wms_events.

In MVP-02 nu se calculeaza final normalized_document_no, canonical_bucket sau economic_sign. Acestea sunt pentru MVP-04 si MVP-05.

## Status import

- SUCCESS: toate randurile sunt valide.
- PARTIAL_SUCCESS: exista randuri valide si randuri respinse.
- FAILED: nu exista randuri valide.

## Endpoint fallback manual

POST /imports/wms/manual

Raspunsul include import_batch_id, source_system, import_type, status, records_imported, records_rejected si error_log.

## Limite MVP-02

Nu include import automat ERP real, normalizare documente, canonicalizare, matching, netare sau verdicturi.
