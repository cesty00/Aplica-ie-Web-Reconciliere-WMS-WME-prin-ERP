from decimal import Decimal

from app.normalization.rules import (
    detect_special_patterns,
    normalize_document,
    normalize_lot_code,
    normalize_partner,
    normalize_product_code,
    normalize_quantity,
)


def test_normalize_sfa_document_removes_prefix() -> None:
    result = normalize_document("SFA45585")

    assert result.raw_value == "SFA45585"
    assert result.normalized_value == "45585"
    assert result.removed_prefix == "SFA"


def test_detect_ret_wme_pattern_from_order() -> None:
    flags = detect_special_patterns(order_no="RET_WME_45585")

    assert flags.is_ret_wme_return is True


def test_detect_wme_doc_minus_one_pattern() -> None:
    flags = detect_special_patterns(order_no="WME45585-1")

    assert flags.is_wme_doc_minus_one_return is True


def test_detect_anulare_comanda_from_reason_or_details() -> None:
    flags = detect_special_patterns(reason_code="ANULARE COMANDA")

    assert flags.is_anulare_comanda is True


def test_normalize_product_lot_partner_and_quantity() -> None:
    assert normalize_product_code(" ds001 ").normalized_value == "DS001"
    assert normalize_lot_code(" lot-1 ").normalized_value == "LOT-1"
    assert normalize_partner(" client   test ").normalized_value == "CLIENT TEST"
    assert normalize_quantity("12,50").normalized_value == Decimal("12.50")
