from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

import pandas as pd

from app.imports.wms_schema import (
    WMS_FIELD_ALIASES,
    WMS_REQUIRED_FIELDS,
    WmsImportError,
    WmsImportRow,
    WmsParseResult,
)


class UnsupportedWmsFileError(ValueError):
    """Raised when a WMS source file has an unsupported extension."""


def parse_wms_file(path: str | Path) -> WmsParseResult:
    """Parse a WMS CSV/XLSX file into validated import rows."""
    file_path = Path(path)
    dataframe = _read_source_file(file_path)
    return parse_wms_dataframe(dataframe)


def parse_wms_dataframe(dataframe: pd.DataFrame) -> WmsParseResult:
    """Parse a dataframe using WMS field aliases and row-level validation."""
    normalized_columns = _build_column_map(dataframe.columns)
    rows: list[WmsImportRow] = []
    errors: list[WmsImportError] = []

    missing_fields = WMS_REQUIRED_FIELDS - set(normalized_columns)
    if missing_fields:
        return WmsParseResult(
            rows=[],
            errors=[
                WmsImportError(
                    source_row=0,
                    field=field,
                    message="Missing required WMS column",
                )
                for field in sorted(missing_fields)
            ],
        )

    for index, raw_row in dataframe.iterrows():
        source_row = int(index) + 2
        parsed_row, row_errors = _parse_row(raw_row.to_dict(), normalized_columns, source_row)
        if row_errors:
            errors.extend(row_errors)
            continue
        rows.append(parsed_row)

    return WmsParseResult(rows=rows, errors=errors)


def _read_source_file(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise UnsupportedWmsFileError(f"Unsupported WMS import file type: {suffix}")


def _build_column_map(columns: list[str] | pd.Index) -> dict[str, str]:
    normalized_input = {_normalize_header(column): column for column in columns}
    result: dict[str, str] = {}

    for canonical_field, aliases in WMS_FIELD_ALIASES.items():
        for alias in aliases:
            normalized_alias = _normalize_header(alias)
            if normalized_alias in normalized_input:
                result[canonical_field] = normalized_input[normalized_alias]
                break

    return result


def _parse_row(
    raw_row: dict[str, Any],
    column_map: dict[str, str],
    source_row: int,
) -> tuple[WmsImportRow, list[WmsImportError]]:
    errors: list[WmsImportError] = []

    product_code = _optional_string(raw_row.get(column_map["product_code"]))
    event_date_raw = raw_row.get(column_map["event_date"])
    raw_operation_type = _optional_string(raw_row.get(column_map["raw_operation_type"]))
    quantity_raw = raw_row.get(column_map["quantity"])

    if not product_code:
        errors.append(WmsImportError(source_row, "product_code", "Product code is required"))
    if not raw_operation_type:
        errors.append(WmsImportError(source_row, "raw_operation_type", "Operation type is required"))

    event_date = _parse_date(event_date_raw)
    if event_date is None:
        errors.append(WmsImportError(source_row, "event_date", "Invalid or missing event date", event_date_raw))

    quantity = _parse_decimal(quantity_raw)
    if quantity is None:
        errors.append(WmsImportError(source_row, "quantity", "Invalid or missing quantity", quantity_raw))

    if errors:
        placeholder = WmsImportRow(
            product_code=product_code or "",
            event_date=date.min,
            raw_operation_type=raw_operation_type or "",
            quantity=Decimal("0"),
            source_row=source_row,
        )
        return placeholder, errors

    assert event_date is not None
    assert quantity is not None
    assert product_code is not None
    assert raw_operation_type is not None

    return (
        WmsImportRow(
            product_code=product_code,
            product_name=_get_optional(raw_row, column_map, "product_name"),
            lot_code=_get_optional(raw_row, column_map, "lot_code"),
            event_date=event_date,
            raw_operation_type=raw_operation_type,
            document_no=_get_optional(raw_row, column_map, "document_no"),
            inbound_document_no=_get_optional(raw_row, column_map, "inbound_document_no"),
            order_no=_get_optional(raw_row, column_map, "order_no"),
            partner=_get_optional(raw_row, column_map, "partner"),
            location_from=_get_optional(raw_row, column_map, "location_from"),
            location_to=_get_optional(raw_row, column_map, "location_to"),
            quantity=quantity,
            reason_code=_get_optional(raw_row, column_map, "reason_code"),
            details=_get_optional(raw_row, column_map, "details"),
            source_row=source_row,
        ),
        [],
    )


def _normalize_header(value: Any) -> str:
    return str(value).strip().lower().replace("_", " ").replace("-", " ")


def _optional_string(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None
    text = str(value).strip()
    return text or None


def _get_optional(raw_row: dict[str, Any], column_map: dict[str, str], field: str) -> str | None:
    column = column_map.get(field)
    if column is None:
        return None
    return _optional_string(raw_row.get(column))


def _parse_date(value: Any) -> date | None:
    if value is None or pd.isna(value):
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    parsed = pd.to_datetime(value, errors="coerce", dayfirst=True)
    if pd.isna(parsed):
        return None
    return parsed.date()


def _parse_decimal(value: Any) -> Decimal | None:
    if value is None or pd.isna(value):
        return None
    try:
        return Decimal(str(value).replace(",", ".").strip())
    except (InvalidOperation, ValueError):
        return None
