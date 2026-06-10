from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.normalization.service import normalize_wme_events_for_batch, normalize_wms_events_for_batch

router = APIRouter(prefix="/normalization", tags=["normalization"])


@router.post("/wms/batches/{import_batch_id}")
def normalize_wms_batch(import_batch_id: int, db: Session = Depends(get_db)) -> dict[str, int | str]:
    """Normalize WMS events for an import batch."""
    normalized_count = normalize_wms_events_for_batch(db, import_batch_id)
    return {
        "source_system": "WMS",
        "import_batch_id": import_batch_id,
        "normalized_events": normalized_count,
    }


@router.post("/wme/batches/{import_batch_id}")
def normalize_wme_batch(import_batch_id: int, db: Session = Depends(get_db)) -> dict[str, int | str]:
    """Normalize WME events for an import batch."""
    normalized_count = normalize_wme_events_for_batch(db, import_batch_id)
    return {
        "source_system": "WME",
        "import_batch_id": import_batch_id,
        "normalized_events": normalized_count,
    }
