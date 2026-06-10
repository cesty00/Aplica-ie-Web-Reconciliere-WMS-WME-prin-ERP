# Model de date initial

## 1. Obiectiv

Acest document defineste modelul de date initial pentru aplicatia de reconciliere WMS-WME prin ERP.

Modelul este orientat pe evenimente economice, nu pe totaluri brute de stoc.

## 2. Entitati principale

### 2.1 products

Tabela produselor reconciliate.

Campuri estimate:

- id
- product_code
- product_name
- category
- unit
- is_finished_good
- is_raw_material
- is_packaging
- active
- created_at
- updated_at

### 2.2 lots

Tabela loturilor asociate produselor.

Campuri estimate:

- id
- product_id
- lot_code
- supplier_lot
- production_date
- expiry_date
- status
- created_at
- updated_at

### 2.3 import_batches

Tabela loturilor de import.

Campuri estimate:

- id
- source_system
- import_type
- period_from
- period_to
- status
- records_imported
- records_rejected
- error_log
- started_at
- completed_at
- created_by

Valori source_system:

- WMS
- WME
- ERP
- MANUAL_UPLOAD

Valori import_type:

- AUTOMATIC
- MANUAL
- TEST

### 2.4 wms_events

Tabela evenimentelor importate din WMS.

Campuri estimate:

- id
- import_batch_id
- product_code
- product_name
- lot_code
- event_date
- raw_operation_type
- canonical_bucket
- document_no
- normalized_document_no
- inbound_document_no
- order_no
- partner
- location_from
- location_to
- quantity
- economic_sign
- reason_code
- details
- source_file
- source_row
- created_at

### 2.5 wme_events

Tabela evenimentelor importate din WME.

Campuri estimate:

- id
- import_batch_id
- product_code
- product_name
- lot_code
- event_date
- document_type
- document_no
- normalized_document_no
- warehouse
- partner
- quantity_in
- quantity_out
- quantity_signed
- stock_after
- canonical_bucket
- economic_sign
- notes
- source_file
- source_row
- created_at

### 2.6 reconciliation_runs

Tabela rularilor de reconciliere.

Campuri estimate:

- id
- product_code
- lot_code
- date_from
- date_to
- run_status
- import_batch_wms_id
- import_batch_wme_id
- created_by
- created_at
- completed_at
- conclusion

Valori run_status:

- DRAFT
- IN_PROGRESS
- NEEDS_REVIEW
- COMPLETED
- BLOCKED
- REOPENED

### 2.7 reconciliation_matches

Tabela legaturilor dintre evenimente WMS si WME.

Campuri estimate:

- id
- reconciliation_run_id
- wms_event_id
- wme_event_id
- match_type
- verdict
- confidence_score
- rule_applied
- quantity_difference
- date_difference_days
- notes
- reviewed_by
- reviewed_at
- created_at

Valori match_type:

- EXACT
- NORMALIZED_DOCUMENT
- DATE_QUANTITY
- PARTNER_DATE_QUANTITY
- PRODUCTION_COMMAND
- NETTED
- MANUAL

Valori verdict:

- MATCH
- MATCH_AFTER_NETTING
- REVIEW
- NOT_MATCH

### 2.8 audit_logs

Tabela istoricului de audit.

Campuri estimate:

- id
- entity_type
- entity_id
- action
- old_value
- new_value
- reason
- user_id
- created_at

## 3. Reguli generale model

1. Datele brute importate trebuie pastrate.
2. Datele normalizate trebuie pastrate separat de datele brute.
3. Orice verdict trebuie sa indice regula aplicata.
4. Orice modificare manuala trebuie sa aiba utilizator si observatie.
5. Evenimentele WMS si WME nu se sterg fizic dupa import; se marcheaza prin status sau import batch.
6. Aplicatia MVP este read-only fata de sistemele sursa.

## 4. Observatii pentru implementare

Modelul initial trebuie sa permita extindere ulterioara pentru:

- reconciliere multi-lot;
- reconciliere multi-produs;
- workflow aprobare;
- export audit;
- scor de incredere avansat;
- reguli configurabile.
