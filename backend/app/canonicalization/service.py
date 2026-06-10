from sqlalchemy.orm import Session

from app.canonicalization.rules import classify_wme_event, classify_wms_event
from app.db.models import WmeEvent, WmsEvent


def canonicalize_wms_event(event: WmsEvent) -> WmsEvent:
    """Assign a canonical bucket to a WMS event without matching or final verdicts."""
    decision = classify_wms_event(event)
    event.canonical_bucket = decision.bucket.value
    event.details = _append_rule_marker(event.details, decision.rule_applied)
    return event


def canonicalize_wme_event(event: WmeEvent) -> WmeEvent:
    """Assign a canonical bucket to a WME event without matching or final verdicts."""
    decision = classify_wme_event(event)
    event.canonical_bucket = decision.bucket.value
    event.notes = _append_rule_marker(event.notes, decision.rule_applied)
    return event


def canonicalize_wms_events_for_batch(db: Session, import_batch_id: int) -> int:
    """Canonicalize all WMS events for an import batch."""
    events = db.query(WmsEvent).filter(WmsEvent.import_batch_id == import_batch_id).all()
    for event in events:
        canonicalize_wms_event(event)
    db.commit()
    return len(events)


def canonicalize_wme_events_for_batch(db: Session, import_batch_id: int) -> int:
    """Canonicalize all WME events for an import batch."""
    events = db.query(WmeEvent).filter(WmeEvent.import_batch_id == import_batch_id).all()
    for event in events:
        canonicalize_wme_event(event)
    db.commit()
    return len(events)


def _append_rule_marker(current_value: str | None, rule_applied: str) -> str:
    marker = f"canonical_rule:{rule_applied}"
    if not current_value:
        return marker
    if marker in current_value:
        return current_value
    return f"{current_value}; {marker}"
