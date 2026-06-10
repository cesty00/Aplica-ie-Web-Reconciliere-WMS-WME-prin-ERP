from sqlalchemy.orm import Session

from app.db.models import EconomicSign, WmeEvent, WmsEvent
from app.normalization.rules import (
    detect_special_patterns,
    normalize_document,
    normalize_lot_code,
    normalize_partner,
    normalize_product_code,
    normalize_quantity,
)


def normalize_wms_event(event: WmsEvent) -> WmsEvent:
    """Normalize a WMS event in-place without assigning final matching verdicts."""
    product = normalize_product_code(event.product_code)
    lot = normalize_lot_code(event.lot_code)
    document = normalize_document(event.document_no)
    partner = normalize_partner(event.partner)
    quantity = normalize_quantity(event.quantity)
    flags = detect_special_patterns(
        document_no=event.document_no,
        order_no=event.order_no,
        reason_code=event.reason_code,
        details=event.details,
    )

    if product.normalized_value:
        event.product_code = product.normalized_value
    event.lot_code = lot.normalized_value
    event.normalized_document_no = document.normalized_value
    event.partner = partner.normalized_value
    if quantity.normalized_value is not None:
        event.quantity = quantity.normalized_value

    event.economic_sign = _infer_wms_sign(event.quantity)
    event.details = _append_normalization_flags(event.details, flags)
    return event


def normalize_wme_event(event: WmeEvent) -> WmeEvent:
    """Normalize a WME event in-place without assigning final matching verdicts."""
    product = normalize_product_code(event.product_code)
    lot = normalize_lot_code(event.lot_code)
    document = normalize_document(event.document_no)
    partner = normalize_partner(event.partner)
    quantity_in = normalize_quantity(event.quantity_in)
    quantity_out = normalize_quantity(event.quantity_out)
    stock_after = normalize_quantity(event.stock_after)

    if product.normalized_value:
        event.product_code = product.normalized_value
    event.lot_code = lot.normalized_value
    event.normalized_document_no = document.normalized_value
    event.partner = partner.normalized_value
    if quantity_in.normalized_value is not None:
        event.quantity_in = quantity_in.normalized_value
    if quantity_out.normalized_value is not None:
        event.quantity_out = quantity_out.normalized_value
    if stock_after.normalized_value is not None:
        event.stock_after = stock_after.normalized_value

    event.quantity_signed = event.quantity_in - event.quantity_out
    event.economic_sign = _infer_wme_sign(event.quantity_signed)
    return event


def normalize_wms_events_for_batch(db: Session, import_batch_id: int) -> int:
    """Normalize all WMS events for an import batch."""
    events = db.query(WmsEvent).filter(WmsEvent.import_batch_id == import_batch_id).all()
    for event in events:
        normalize_wms_event(event)
    db.commit()
    return len(events)


def normalize_wme_events_for_batch(db: Session, import_batch_id: int) -> int:
    """Normalize all WME events for an import batch."""
    events = db.query(WmeEvent).filter(WmeEvent.import_batch_id == import_batch_id).all()
    for event in events:
        normalize_wme_event(event)
    db.commit()
    return len(events)


def _infer_wms_sign(quantity) -> EconomicSign:
    if quantity is None:
        return EconomicSign.UNKNOWN
    if quantity > 0:
        return EconomicSign.IN
    if quantity < 0:
        return EconomicSign.OUT
    return EconomicSign.NEUTRAL


def _infer_wme_sign(quantity_signed) -> EconomicSign:
    if quantity_signed is None:
        return EconomicSign.UNKNOWN
    if quantity_signed > 0:
        return EconomicSign.IN
    if quantity_signed < 0:
        return EconomicSign.OUT
    return EconomicSign.NEUTRAL


def _append_normalization_flags(details: str | None, flags) -> str | None:
    markers: list[str] = []
    if flags.is_sfa_document:
        markers.append("normalized:SFA_DOCUMENT")
    if flags.is_ret_wme_return:
        markers.append("pattern:RET_WME")
    if flags.is_wme_doc_minus_one_return:
        markers.append("pattern:WME_DOC_MINUS_ONE")
    if flags.is_anulare_comanda:
        markers.append("pattern:ANULARE_COMANDA")

    if not markers:
        return details

    suffix = "; ".join(markers)
    return f"{details}; {suffix}" if details else suffix
