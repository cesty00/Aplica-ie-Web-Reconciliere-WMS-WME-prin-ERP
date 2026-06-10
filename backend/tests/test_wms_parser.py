from decimal import Decimal

import pandas as pd

from app.imports.wms_parser import parse_wms_dataframe


def test_parse_wms_dataframe_with_valid_aliases() -> None:
    dataframe = pd.DataFrame(
        [
            {
                "Cod Produs": "DS001",
                "Denumire Produs": "Produs test",
                "Lot": "LOT-1",
                "Data Operatiune": "10.06.2026",
                "Tip Operatiune": "Receptie",
                "Document": "SFA45585",
                "Numar Comanda": "CMD-1",
                "Cantitate": "12,5",
                "Cod Motiv": "",
                "Detalii": "test",
            }
        ]
    )

    result = parse_wms_dataframe(dataframe)

    assert result.errors == []
    assert len(result.rows) == 1
    row = result.rows[0]
    assert row.product_code == "DS001"
    assert row.product_name == "Produs test"
    assert row.lot_code == "LOT-1"
    assert row.raw_operation_type == "Receptie"
    assert row.document_no == "SFA45585"
    assert row.order_no == "CMD-1"
    assert row.quantity == Decimal("12.5")


def test_parse_wms_dataframe_reports_missing_required_columns() -> None:
    dataframe = pd.DataFrame([{"Cod Produs": "DS001"}])

    result = parse_wms_dataframe(dataframe)

    assert result.rows == []
    assert {error.field for error in result.errors} == {
        "event_date",
        "quantity",
        "raw_operation_type",
    }


def test_parse_wms_dataframe_rejects_invalid_row_values() -> None:
    dataframe = pd.DataFrame(
        [
            {
                "Cod Produs": "",
                "Data Operatiune": "not-a-date",
                "Tip Operatiune": "Livrare",
                "Cantitate": "not-a-number",
            }
        ]
    )

    result = parse_wms_dataframe(dataframe)

    assert result.rows == []
    assert {error.field for error in result.errors} == {
        "product_code",
        "event_date",
        "quantity",
    }
