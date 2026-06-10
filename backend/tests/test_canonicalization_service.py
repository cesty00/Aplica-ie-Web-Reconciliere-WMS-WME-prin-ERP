from datetime import date
from decimal import Decimal

from app.canonicalization.buckets import CanonicalBucket
from app.canonicalization.service import canonicalize_wme_event, canonicalize_wms_event
from app.db.models import EconomicSign, WmeEvent, WmsEvent


def test_canonicalize_wms_event_sets_bucket_and_rule_marker() -> None:
    event = WmsEvent(
        import_batch_id=1,
        product_code="DS001",
        event_date=date(2026, 6, 10),
        raw_operation_type="Receptie",
        quantity=Decimal("10"),
        economic_sign=EconomicSign.IN,
    )

    canonicalize_wms_event(event)

    assert event.canonical_bucket == CanonicalBucket.RECEIPT.value
    assert "canonical_rule:WMS_RECEIPT" in event.details


def test_canonicalize_wme_event_sets_bucket_and_rule_marker() -> None:
    event = WmeEvent(
        import_batch_id=1,
        product_code="DS001",
        event_date=date(2026, 6, 10),
        document_type="BC",
        document_no="BC1",
        quantity_in=Decimal("0"),
        quantity_out=Decimal("10"),
        quantity_signed=Decimal("-10"),
        economic_sign=EconomicSign.OUT,
    )

    canonicalize_wme_event(event)

    assert event.canonical_bucket == CanonicalBucket.PRODUCTION_CONSUMPTION.value
    assert "canonical_rule:WME_BC_CONSUMPTION" in event.notes
