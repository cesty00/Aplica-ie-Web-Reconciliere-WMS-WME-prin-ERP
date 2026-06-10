import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any


SFA_PREFIX_RE = re.compile(r"^SFA\s*[-_/]*\s*(?P<doc>.+)$", re.IGNORECASE)
RET_WME_RE = re.compile(r"^RET[_\-\s]*WME", re.IGNORECASE)
WME_RETURN_RE = re.compile(r"^WME(?P<doc>.+)-1$", re.IGNORECASE)
ANULARE_COMANDA_RE = re.compile(r"ANULARE\s+COMANDA", re.IGNORECASE)


@dataclass(frozen=True)
class NormalizedDocument:
    raw_value: str | None
    normalized_value: str | None
    removed_prefix: str | None = None
    is_ret_wme: bool = False
    is_wme_return_pattern: bool = False


@dataclass(frozen=True)
class NormalizedText:
    raw_value: str | None
    normalized_value: str | None


@dataclass(frozen=True)
class NormalizedQuantity:
    raw_value: Any | None
    normalized_value: Decimal | None


@dataclass(frozen=True)
class SpecialPatternFlags:
    is_sfa_document: bool = False
    is_ret_wme_return: bool = False
    is_wme_doc_minus_one_return: bool = False
    is_anulare_comanda: bool = False


def normalize_document(value: Any | None) -> NormalizedDocument:
    raw = _to_text(value)
    if raw is None:
        return NormalizedDocument(raw_value=None, normalized_value=None)

    compact = _collapse_spaces(raw)
    sfa_match = SFA_PREFIX_RE.match(compact)
    if sfa_match:
        return NormalizedDocument(
            raw_value=raw,
            normalized_value=_collapse_spaces(sfa_match.group("doc")),
            removed_prefix="SFA",
        )

    ret_wme = bool(RET_WME_RE.match(compact))
    wme_return = bool(WME_RETURN_RE.match(compact))

    return NormalizedDocument(
        raw_value=raw,
        normalized_value=compact,
        is_ret_wme=ret_wme,
        is_wme_return_pattern=wme_return,
    )


def normalize_product_code(value: Any | None) -> NormalizedText:
    raw = _to_text(value)
    return NormalizedText(raw_value=raw, normalized_value=raw.upper() if raw else None)


def normalize_lot_code(value: Any | None) -> NormalizedText:
    raw = _to_text(value)
    return NormalizedText(raw_value=raw, normalized_value=raw.upper() if raw else None)


def normalize_partner(value: Any | None) -> NormalizedText:
    raw = _to_text(value)
    return NormalizedText(raw_value=raw, normalized_value=_collapse_spaces(raw).upper() if raw else None)


def normalize_quantity(value: Any | None) -> NormalizedQuantity:
    if value is None:
        return NormalizedQuantity(raw_value=None, normalized_value=None)
    try:
        normalized = Decimal(str(value).replace(",", ".").strip())
    except (InvalidOperation, ValueError):
        normalized = None
    return NormalizedQuantity(raw_value=value, normalized_value=normalized)


def detect_special_patterns(
    *,
    document_no: Any | None = None,
    order_no: Any | None = None,
    reason_code: Any | None = None,
    details: Any | None = None,
) -> SpecialPatternFlags:
    document = normalize_document(document_no)
    order_text = _to_text(order_no) or ""
    reason_text = _to_text(reason_code) or ""
    details_text = _to_text(details) or ""
    combined_reason = f"{reason_text} {details_text}"

    order_document = normalize_document(order_text)

    return SpecialPatternFlags(
        is_sfa_document=document.removed_prefix == "SFA",
        is_ret_wme_return=document.is_ret_wme or order_document.is_ret_wme,
        is_wme_doc_minus_one_return=document.is_wme_return_pattern or order_document.is_wme_return_pattern,
        is_anulare_comanda=bool(ANULARE_COMANDA_RE.search(combined_reason)),
    )


def _to_text(value: Any | None) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _collapse_spaces(value: str) -> str:
    return " ".join(value.strip().split())
