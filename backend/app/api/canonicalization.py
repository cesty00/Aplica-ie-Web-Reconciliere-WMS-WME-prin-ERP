from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.canonicalization.service import (
    canonicalize_wme_events_for_batch,
    canonicalize_wms_events_for_batch,
)
from app.db.session import get_db

router = APIRouter(prefix="/canonicalization", tags=["canonicalization"])


@router.post("/wms/batches/{import_batch_id}")
def canonicalize_wms_batch(import_batch_id: int, db: Session = Depends(get_db)) -> dict[str, int | str]:
    """Canonicalize WMS events for an import batch."""
    canonicalized_count = canonicalize_wms_events_for_batch(db, import_batch_id)
    return {
        "source_system": "WMS",
        "import_batch_id": import_batch_id,
        "canonicalized_events": canonicalized_count,
    }


@router.post("/wme/batches/{import_batch_id}")
def canonicalize_wme_batch(import_batch_id: int, db: Session = Depends(get_db)) -> dict[str, int | str]:
    """Canonicalize WME events for an import batch."""
    canonicalized_count = canonicalize_wme_events_for_batch(db, import_batch_id)
    return {
        "source_system": "WME",
        "import_batch_id": import_batch_id,
        "canonicalized_events": canonicalized_count,
    }
