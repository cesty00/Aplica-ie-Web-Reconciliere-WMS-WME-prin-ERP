from decimal import Decimal

import pandas as pd

from app.imports.wme_parser import parse_wme_dataframe


def test_parse_wme_dataframe_with_valid_aliases_and_signed_quantity() -> None:
    dataframe = pd.DataFrame(
        [
            {
                "Cod Articol": "DS001",
                "Denumire Produs": "Produs test",
                "Lot": "LOT-1",
                "Data Document": "10.06.2026",
                "Tip Document": "AE",
                "Nr Document": "45585",
                "Gestiune": "3711",
                "Partener": "CLIENT TEST",
                "Intrare": "0",
                "Iesire": "12,5",
                "Stoc": "100",
                "Observatii": "test",
            }
        ]
    )

    result = parse_wme_dataframe(dataframe)

    assert result.errors == []
    assert len(result.rows) == 1
    row = result.rows[0]
    assert row.product_code == "DS001"
    assert row.product_name == "Produs test"
    assert row.lot_code == "LOT-1"
    assert row.document_type == "AE"
    assert row.document_no == "45585"
    assert row.warehouse == "3711"
    assert row.partner == "CLIENT TEST"
    assert row.quantity_in == Decimal("0")
    assert row.quantity_out == Decimal("12.5")
    assert row.quantity_signed == Decimal("-12.5")
    assert row.stock_after == Decimal("100")


def test_parse_wme_dataframe_reports_missing_required_columns() -> None:
    dataframe = pd.DataFrame([{"Cod Articol": "DS001", "Intrare": "1"}])

    result = parse_wme_dataframe(dataframe)

    assert result.rows == []
    assert {error.field for error in result.errors} == {
        "document_no",
        "document_type",
        "event_date",
    }


def test_parse_wme_dataframe_requires_non_zero_quantity() -> None:
    dataframe = pd.DataFrame(
        [
            {
                "Cod Articol": "DS001",
                "Data Document": "10.06.2026",
                "Tip Document": "AE",
                "Nr Document": "45585",
                "Intrare": "0",
                "Iesire": "0",
            }
        ]
    )

    result = parse_wme_dataframe(dataframe)

    assert result.rows == []
    assert {error.field for error in result.errors} == {"quantity_in|quantity_out"}


def test_parse_wme_dataframe_rejects_invalid_date_and_quantity() -> None:
    dataframe = pd.DataFrame(
        [
            {
                "Cod Articol": "DS001",
                "Data Document": "not-a-date",
                "Tip Document": "AE",
                "Nr Document": "45585",
                "Intrare": "abc",
                "Iesire": "0",
            }
        ]
    )

    result = parse_wme_dataframe(dataframe)

    assert result.rows == []
    assert {error.field for error in result.errors} == {"event_date", "quantity_in"}
