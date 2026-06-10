from datetime import date
from decimal import Decimal

from app.canonicalization.buckets import CanonicalBucket
from app.canonicalization.rules import classify_wme_event, classify_wms_event
from app.db.models import EconomicSign, WmeEvent, WmsEvent


def test_classify_wms_receipt() -> None:
    event = WmsEvent(
        import_batch_id=1,
        product_code="DS001",
        event_date=date(2026, 6, 10),
        raw_operation_type="Receptie",
        quantity=Decimal("10"),
        economic_sign=EconomicSign.IN,
    )

    decision = classify_wms_event(event)

    assert decision.bucket == CanonicalBucket.RECEIPT
    assert decision.rule_applied == "WMS_RECEIPT"


def test_classify_wms_return_pattern() -> None:
    event = WmsEvent(
        import_batch_id=1,
        product_code="DS001",
        event_date=date(2026, 6, 10),
        raw_operation_type="Livrare",
        document_no="RET_WME_45585",
        quantity=Decimal("10"),
        economic_sign=EconomicSign.IN,
    )

    decision = classify_wms_event(event)

    assert decision.bucket == CanonicalBucket.RETURN_IN
    assert decision.rule_applied == "WMS_RETURN_PATTERN"


def test_classify_wms_anulare_comanda() -> None:
    event = WmsEvent(
        import_batch_id=1,
        product_code="DS001",
        event_date=date(2026, 6, 10),
        raw_operation_type="Ajustare",
        reason_code="ANULARE COMANDA",
        quantity=Decimal("10"),
        economic_sign=EconomicSign.IN,
    )

    decision = classify_wms_event(event)

    assert decision.bucket == CanonicalBucket.DELIVERY_REVERSAL
    assert decision.rule_applied == "WMS_ANULARE_COMANDA"


def test_classify_wme_ae_delivery_and_return() -> None:
    outbound = WmeEvent(
        import_batch_id=1,
        product_code="DS001",
        event_date=date(2026, 6, 10),
        document_type="AE",
        document_no="45585",
        quantity_in=Decimal("0"),
        quantity_out=Decimal("10"),
        quantity_signed=Decimal("-10"),
        economic_sign=EconomicSign.OUT,
    )
    inbound = WmeEvent(
        import_batch_id=1,
        product_code="DS001",
        event_date=date(2026, 6, 10),
        document_type="AE",
        document_no="45586",
        quantity_in=Decimal("10"),
        quantity_out=Decimal("0"),
        quantity_signed=Decimal("10"),
        economic_sign=EconomicSign.IN,
    )

    assert classify_wme_event(outbound).bucket == CanonicalBucket.DELIVERY
    assert classify_wme_event(inbound).bucket == CanonicalBucket.RETURN_IN


def test_classify_wme_production_documents() -> None:
    bc = WmeEvent(
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
    np = WmeEvent(
        import_batch_id=1,
        product_code="DS001",
        event_date=date(2026, 6, 10),
        document_type="NP",
        document_no="NP1",
        quantity_in=Decimal("10"),
        quantity_out=Decimal("0"),
        quantity_signed=Decimal("10"),
        economic_sign=EconomicSign.IN,
    )

    assert classify_wme_event(bc).bucket == CanonicalBucket.PRODUCTION_CONSUMPTION
    assert classify_wme_event(np).bucket == CanonicalBucket.FINISHED_GOOD_OUTPUT
