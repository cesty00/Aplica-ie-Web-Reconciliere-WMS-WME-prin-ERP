from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from app.db.models import EconomicSign, ImportBatch, ImportStatus, ImportType, SourceSystem, WmsEvent
from app.imports.wms_parser import parse_wms_file
from app.imports.wms_schema import WmsImportRow


def import_wms_file(
    db: Session,
    path: str | Path,
    *,
    import_type: ImportType = ImportType.MANUAL,
    created_by: str | None = None,
) -> ImportBatch:
    """Import WMS rows from a file into the application database.

    This is read-only against WMS. It only persists imported data in the reconciliation database.
    """
    batch = ImportBatch(
        source_system=SourceSystem.WMS,
        import_type=import_type,
        status=ImportStatus.RUNNING,
        started_at=datetime.utcnow(),
        created_by=created_by,
    )
    db.add(batch)
    db.flush()

    result = parse_wms_file(path)

    for row in result.rows:
        db.add(_build_wms_event(batch.id, row, source_file=str(path)))

    batch.records_imported = len(result.rows)
    batch.records_rejected = len(result.errors)
    batch.error_log = _format_errors(result.errors)
    batch.status = _resolve_status(len(result.rows), len(result.errors))
    batch.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(batch)
    return batch


def _build_wms_event(import_batch_id: int, row: WmsImportRow, *, source_file: str) -> WmsEvent:
    return WmsEvent(
        import_batch_id=import_batch_id,
        product_code=row.product_code,
        product_name=row.product_name,
        lot_code=row.lot_code,
        event_date=row.event_date,
        raw_operation_type=row.raw_operation_type,
        canonical_bucket=None,
        document_no=row.document_no,
        normalized_document_no=None,
        inbound_document_no=row.inbound_document_no,
        order_no=row.order_no,
        partner=row.partner,
        location_from=row.location_from,
        location_to=row.location_to,
        quantity=row.quantity,
        economic_sign=EconomicSign.UNKNOWN,
        reason_code=row.reason_code,
        details=row.details,
        source_file=source_file,
        source_row=row.source_row,
    )


def _resolve_status(records_imported: int, records_rejected: int) -> ImportStatus:
    if records_imported > 0 and records_rejected == 0:
        return ImportStatus.SUCCESS
    if records_imported > 0 and records_rejected > 0:
        return ImportStatus.PARTIAL_SUCCESS
    return ImportStatus.FAILED


def _format_errors(errors: object) -> str | None:
    error_list = list(errors)
    if not error_list:
        return None
    return "\n".join(
        f"row={error.source_row}; field={error.field}; message={error.message}; raw={error.raw_value}"
        for error in error_list
    )
