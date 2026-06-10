from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any


WMS_REQUIRED_FIELDS = {
    "product_code",
    "event_date",
    "raw_operation_type",
    "quantity",
}

WMS_FIELD_ALIASES = {
    "product_code": ["product_code", "cod produs", "cod_produs", "cod articol", "cod_articol"],
    "product_name": ["product_name", "denumire produs", "denumire_produs", "descriere"],
    "lot_code": ["lot_code", "lot", "lot produs", "lot_produs"],
    "event_date": ["event_date", "data", "data operatiune", "data_operatiune", "data miscare"],
    "raw_operation_type": ["raw_operation_type", "tip operatiune", "tip_operatiune", "operatiune"],
    "document_no": ["document_no", "document", "nr document", "numar document"],
    "inbound_document_no": ["inbound_document_no", "document intrare", "document_intrare"],
    "order_no": ["order_no", "numar comanda", "numar_comanda", "comanda"],
    "partner": ["partner", "partener", "client", "furnizor"],
    "location_from": ["location_from", "locatie sursa", "locatie_sursa", "de la"],
    "location_to": ["location_to", "locatie destinatie", "locatie_destinatie", "la"],
    "quantity": ["quantity", "cantitate", "qty"],
    "reason_code": ["reason_code", "cod motiv", "cod_motiv", "motiv"],
    "details": ["details", "detalii", "observatii"],
}


@dataclass(frozen=True)
class WmsImportRow:
    product_code: str
    event_date: date
    raw_operation_type: str
    quantity: Decimal
    product_name: str | None = None
    lot_code: str | None = None
    document_no: str | None = None
    inbound_document_no: str | None = None
    order_no: str | None = None
    partner: str | None = None
    location_from: str | None = None
    location_to: str | None = None
    reason_code: str | None = None
    details: str | None = None
    source_row: int | None = None


@dataclass(frozen=True)
class WmsImportError:
    source_row: int
    field: str
    message: str
    raw_value: Any | None = None


@dataclass(frozen=True)
class WmsParseResult:
    rows: list[WmsImportRow]
    errors: list[WmsImportError]
