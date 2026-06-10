from datetime import date
from decimal import Decimal

from app.db.models import EconomicSign, WmeEvent, WmsEvent
from app.normalization.service import normalize_wme_event, normalize_wms_event


def test_normalize_wms_event_sets_normalized_document_and_flags() -> None:
    event = WmsEvent(
        import_batch_id=1,
        product_code=" ds001 ",
        lot_code=" lot-1 ",
        event_date=date(2026, 6, 10),
        raw_operation_type="Livrare",
        document_no="SFA45585",
        order_no="RET_WME_45585",
        partner=" client   test ",
        quantity=Decimal("-12.5"),
        reason_code="ANULARE COMANDA",
    )

    normalize_wms_event(event)

    assert event.product_code == "DS001"
    assert event.lot_code == "LOT-1"
    assert event.normalized_document_no == "45585"
    assert event.partner == "CLIENT TEST"
    assert event.economic_sign == EconomicSign.OUT
    assert "normalized:SFA_DOCUMENT" in event.details
    assert "pattern:RET_WME" in event.details
    assert "pattern:ANULARE_COMANDA" in event.details


def test_normalize_wme_event_recalculates_signed_quantity_and_sign() -> None:
    event = WmeEvent(
        import_batch_id=1,
        product_code=" ds001 ",
        lot_code=" lot-1 ",
        event_date=date(2026, 6, 10),
        document_type="AE",
        document_no="SFA45585",
        warehouse="3711",
        partner=" client   test ",
        quantity_in=Decimal("0"),
        quantity_out=Decimal("12.5"),
        quantity_signed=Decimal("0"),
    )

    normalize_wme_event(event)

    assert event.product_code == "DS001"
    assert event.lot_code == "LOT-1"
    assert event.normalized_document_no == "45585"
    assert event.partner == "CLIENT TEST"
    assert event.quantity_signed == Decimal("-12.5")
    assert event.economic_sign == EconomicSign.OUT
