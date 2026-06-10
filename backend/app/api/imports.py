from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db.models import ImportBatch, ImportType
from app.db.session import get_db
from app.imports.wms_import_service import import_wms_file
from app.imports.wms_parser import UnsupportedWmsFileError

router = APIRouter(prefix="/imports", tags=["imports"])


@router.post("/wms/manual", status_code=status.HTTP_201_CREATED)
def upload_wms_manual_import(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> dict[str, int | str | None]:
    """Fallback manual WMS upload endpoint.

    The main project flow remains automatic ERP-based import. This endpoint is for tests,
    audit checks, and exceptional fallback scenarios.
    """
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".csv", ".xlsx", ".xls"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported WMS import file type. Use CSV or XLSX.",
        )

    try:
        with NamedTemporaryFile(delete=True, suffix=suffix) as temporary_file:
            temporary_file.write(file.file.read())
            temporary_file.flush()
            batch: ImportBatch = import_wms_file(
                db,
                temporary_file.name,
                import_type=ImportType.MANUAL,
                created_by="manual-upload",
            )
    except UnsupportedWmsFileError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return {
        "import_batch_id": batch.id,
        "source_system": batch.source_system.value,
        "import_type": batch.import_type.value,
        "status": batch.status.value,
        "records_imported": batch.records_imported,
        "records_rejected": batch.records_rejected,
        "error_log": batch.error_log,
    }
