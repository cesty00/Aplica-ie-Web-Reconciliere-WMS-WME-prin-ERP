from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any


WME_REQUIRED_FIELDS = {
    "product_code",
    "event_date",
    "document_type",
    "document_no",
}

WME_QUANTITY_FIELDS = {"quantity_in", "quantity_out"}

WME_FIELD_ALIASES = {
    "product_code": ["product_code", "cod produs", "cod_produs", "cod articol", "cod_articol"],
    "product_name": ["product_name", "denumire produs", "denumire_produs", "descriere"],
    "lot_code": ["lot_code", "lot", "lot produs", "lot_produs"],
    "event_date": ["event_date", "data", "data document", "data_document"],
    "document_type": ["document_type", "tip document", "tip_document", "tip doc"],
    "document_no": ["document_no", "document", "nr document", "numar document"],
    "warehouse": ["warehouse", "gestiune", "magazie"],
    "partner": ["partner", "partener", "client", "furnizor"],
    "quantity_in": ["quantity_in", "intrare", "cantitate intrare", "cantitate_intrare"],
    "quantity_out": ["quantity_out", "iesire", "ieșire", "cantitate iesire", "cantitate_iesire"],
    "stock_after": ["stock_after", "stoc", "stoc dupa", "stoc_dupa"],
    "notes": ["notes", "observatii", "explicatii", "detalii"],
}


@dataclass(frozen=True)
class WmeImportRow:
    product_code: str
    event_date: date
    document_type: str
    document_no: str
    quantity_in: Decimal
    quantity_out: Decimal
    quantity_signed: Decimal
    product_name: str | None = None
    lot_code: str | None = None
    warehouse: str | None = None
    partner: str | None = None
    stock_after: Decimal | None = None
    notes: str | None = None
    source_row: int | None = None


@dataclass(frozen=True)
class WmeImportError:
    source_row: int
    field: str
    message: str
    raw_value: Any | None = None


@dataclass(frozen=True)
class WmeParseResult:
    rows: list[WmeImportRow]
    errors: list[WmeImportError]
