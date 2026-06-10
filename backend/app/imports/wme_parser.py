from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

import pandas as pd

from app.imports.wme_schema import (
    WME_FIELD_ALIASES,
    WME_QUANTITY_FIELDS,
    WME_REQUIRED_FIELDS,
    WmeImportError,
    WmeImportRow,
    WmeParseResult,
)


class UnsupportedWmeFileError(ValueError):
    """Raised when a WME source file has an unsupported extension."""


def parse_wme_file(path: str | Path) -> WmeParseResult:
    """Parse a WME CSV/XLSX file into validated import rows."""
    file_path = Path(path)
    dataframe = _read_source_file(file_path)
    return parse_wme_dataframe(dataframe)


def parse_wme_dataframe(dataframe: pd.DataFrame) -> WmeParseResult:
    """Parse a dataframe using WME field aliases and row-level validation."""
    normalized_columns = _build_column_map(dataframe.columns)
    rows: list[WmeImportRow] = []
    errors: list[WmeImportError] = []

    missing_fields = WME_REQUIRED_FIELDS - set(normalized_columns)
    if missing_fields:
        return WmeParseResult(
            rows=[],
            errors=[
                WmeImportError(
                    source_row=0,
                    field=field,
                    message="Missing required WME column",
                )
                for field in sorted(missing_fields)
            ],
        )

    if not WME_QUANTITY_FIELDS.intersection(normalized_columns):
        return WmeParseResult(
            rows=[],
            errors=[
                WmeImportError(
                    source_row=0,
                    field="quantity_in|quantity_out",
                    message="At least one WME quantity column is required",
                )
            ],
        )

    for index, raw_row in dataframe.iterrows():
        source_row = int(index) + 2
        parsed_row, row_errors = _parse_row(raw_row.to_dict(), normalized_columns, source_row)
        if row_errors:
            errors.extend(row_errors)
            continue
        rows.append(parsed_row)

    return WmeParseResult(rows=rows, errors=errors)


def _read_source_file(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise UnsupportedWmeFileError(f"Unsupported WME import file type: {suffix}")


def _build_column_map(columns: list[str] | pd.Index) -> dict[str, str]:
    normalized_input = {_normalize_header(column): column for column in columns}
    result: dict[str, str] = {}

    for canonical_field, aliases in WME_FIELD_ALIASES.items():
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
) -> tuple[WmeImportRow, list[WmeImportError]]:
    errors: list[WmeImportError] = []

    product_code = _optional_string(raw_row.get(column_map["product_code"]))
    event_date_raw = raw_row.get(column_map["event_date"])
    document_type = _optional_string(raw_row.get(column_map["document_type"]))
    document_no = _optional_string(raw_row.get(column_map["document_no"]))

    if not product_code:
        errors.append(WmeImportError(source_row, "product_code", "Product code is required"))
    if not document_type:
        errors.append(WmeImportError(source_row, "document_type", "Document type is required"))
    if not document_no:
        errors.append(WmeImportError(source_row, "document_no", "Document number is required"))

    event_date = _parse_date(event_date_raw)
    if event_date is None:
        errors.append(WmeImportError(source_row, "event_date", "Invalid or missing event date", event_date_raw))

    quantity_in = _parse_decimal(_get_raw(raw_row, column_map, "quantity_in"), default=Decimal("0"))
    quantity_out = _parse_decimal(_get_raw(raw_row, column_map, "quantity_out"), default=Decimal("0"))
    stock_after = _parse_decimal(_get_raw(raw_row, column_map, "stock_after"), default=None)

    if quantity_in is None:
        errors.append(WmeImportError(source_row, "quantity_in", "Invalid quantity_in"))
    if quantity_out is None:
        errors.append(WmeImportError(source_row, "quantity_out", "Invalid quantity_out"))

    if quantity_in == Decimal("0") and quantity_out == Decimal("0"):
        errors.append(
            WmeImportError(
                source_row,
                "quantity_in|quantity_out",
                "At least one quantity must be non-zero",
            )
        )

    if errors:
        placeholder = WmeImportRow(
            product_code=product_code or "",
            event_date=date.min,
            document_type=document_type or "",
            document_no=document_no or "",
            quantity_in=Decimal("0"),
            quantity_out=Decimal("0"),
            quantity_signed=Decimal("0"),
            source_row=source_row,
        )
        return placeholder, errors

    assert event_date is not None
    assert product_code is not None
    assert document_type is not None
    assert document_no is not None
    assert quantity_in is not None
    assert quantity_out is not None

    return (
        WmeImportRow(
            product_code=product_code,
            product_name=_get_optional(raw_row, column_map, "product_name"),
            lot_code=_get_optional(raw_row, column_map, "lot_code"),
            event_date=event_date,
            document_type=document_type,
            document_no=document_no,
            warehouse=_get_optional(raw_row, column_map, "warehouse"),
            partner=_get_optional(raw_row, column_map, "partner"),
            quantity_in=quantity_in,
            quantity_out=quantity_out,
            quantity_signed=quantity_in - quantity_out,
            stock_after=stock_after,
            notes=_get_optional(raw_row, column_map, "notes"),
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


def _get_raw(raw_row: dict[str, Any], column_map: dict[str, str], field: str) -> Any | None:
    column = column_map.get(field)
    if column is None:
        return None
    return raw_row.get(column)


def _get_optional(raw_row: dict[str, Any], column_map: dict[str, str], field: str) -> str | None:
    return _optional_string(_get_raw(raw_row, column_map, field))


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


def _parse_decimal(value: Any, *, default: Decimal | None) -> Decimal | None:
    if value is None or pd.isna(value):
        return default
    try:
        return Decimal(str(value).replace(",", ".").strip())
    except (InvalidOperation, ValueError):
        return None
