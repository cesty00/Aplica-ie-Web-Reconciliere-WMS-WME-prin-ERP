from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from app.db.models import EconomicSign, ImportBatch, ImportStatus, ImportType, SourceSystem, WmeEvent
from app.imports.wme_parser import parse_wme_file
from app.imports.wme_schema import WmeImportRow


def import_wme_file(
    db: Session,
    path: str | Path,
    *,
    import_type: ImportType = ImportType.MANUAL,
    created_by: str | None = None,
) -> ImportBatch:
    """Import WME rows from a file into the application database.

    This is read-only against WME/WinMentor. It only persists imported data in the
    reconciliation database.
    """
    batch = ImportBatch(
        source_system=SourceSystem.WME,
        import_type=import_type,
        status=ImportStatus.RUNNING,
        started_at=datetime.utcnow(),
        created_by=created_by,
    )
    db.add(batch)
    db.flush()

    result = parse_wme_file(path)

    for row in result.rows:
        db.add(_build_wme_event(batch.id, row, source_file=str(path)))

    batch.records_imported = len(result.rows)
    batch.records_rejected = len(result.errors)
    batch.error_log = _format_errors(result.errors)
    batch.status = _resolve_status(len(result.rows), len(result.errors))
    batch.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(batch)
    return batch


def _build_wme_event(import_batch_id: int, row: WmeImportRow, *, source_file: str) -> WmeEvent:
    return WmeEvent(
        import_batch_id=import_batch_id,
        product_code=row.product_code,
        product_name=row.product_name,
        lot_code=row.lot_code,
        event_date=row.event_date,
        document_type=row.document_type,
        document_no=row.document_no,
        normalized_document_no=None,
        warehouse=row.warehouse,
        partner=row.partner,
        quantity_in=row.quantity_in,
        quantity_out=row.quantity_out,
        quantity_signed=row.quantity_signed,
        stock_after=row.stock_after,
        canonical_bucket=None,
        economic_sign=EconomicSign.UNKNOWN,
        notes=row.notes,
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
