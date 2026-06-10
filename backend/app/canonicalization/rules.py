from dataclasses import dataclass
from typing import Any

from app.canonicalization.buckets import CanonicalBucket
from app.db.models import EconomicSign, WmeEvent, WmsEvent
from app.normalization.rules import detect_special_patterns


@dataclass(frozen=True)
class BucketDecision:
    bucket: CanonicalBucket
    rule_applied: str
    reason: str


def classify_wms_event(event: WmsEvent) -> BucketDecision:
    """Classify a normalized WMS event into a canonical economic bucket."""
    operation = _normalized_text(event.raw_operation_type)
    reason = _normalized_text(event.reason_code)
    details = _normalized_text(event.details)
    order_no = _normalized_text(event.order_no)
    location_to = _normalized_text(event.location_to)
    flags = detect_special_patterns(
        document_no=event.document_no,
        order_no=event.order_no,
        reason_code=event.reason_code,
        details=event.details,
    )

    if flags.is_ret_wme_return or flags.is_wme_doc_minus_one_return:
        return BucketDecision(CanonicalBucket.RETURN_IN, "WMS_RETURN_PATTERN", "WMS return pattern detected")

    if flags.is_anulare_comanda:
        return BucketDecision(CanonicalBucket.DELIVERY_REVERSAL, "WMS_ANULARE_COMANDA", "Cancellation of order detected")

    if "COR STOC" in reason or "CORECTIE" in reason or "AJUST" in operation:
        return BucketDecision(CanonicalBucket.ADJUSTMENT, "WMS_ADJUSTMENT", "Stock correction or adjustment")

    if "TRANSFER" in operation or "TRANSFER" in order_no:
        if location_to in {"VER100", "LIV100"}:
            return BucketDecision(CanonicalBucket.TRANSFER_3P, "WMS_TRANSFER_3P", "Transfer to known 3P location")
        return BucketDecision(CanonicalBucket.TRANSFER, "WMS_TRANSFER", "Transfer operation")

    if "PRODUCTION-IN" in operation or "PRODUCTIE-IN" in operation or "CONSUM" in operation:
        return BucketDecision(CanonicalBucket.PRODUCTION_CONSUMPTION, "WMS_PRODUCTION_IN", "Production consumption")

    if "PRODUCTION-OUT" in operation or "PRODUCTIE-OUT" in operation or "PREDARE" in operation:
        return BucketDecision(CanonicalBucket.FINISHED_GOOD_OUTPUT, "WMS_PRODUCTION_OUT", "Finished good output")

    if "RECEPT" in operation:
        return BucketDecision(CanonicalBucket.RECEIPT, "WMS_RECEIPT", "Receipt operation")

    if "LIVRA" in operation or event.economic_sign == EconomicSign.OUT:
        return BucketDecision(CanonicalBucket.DELIVERY, "WMS_DELIVERY", "Delivery operation or negative sign")

    if event.economic_sign == EconomicSign.IN:
        return BucketDecision(CanonicalBucket.RECEIPT, "WMS_POSITIVE_SIGN_RECEIPT", "Positive sign fallback")

    if details:
        return BucketDecision(CanonicalBucket.REVIEW, "WMS_REVIEW_WITH_DETAILS", "Unclear WMS event with details")

    return BucketDecision(CanonicalBucket.REVIEW, "WMS_REVIEW_FALLBACK", "No canonical WMS rule matched")


def classify_wme_event(event: WmeEvent) -> BucketDecision:
    """Classify a normalized WME event into a canonical economic bucket."""
    document_type = _normalized_text(event.document_type)
    notes = _normalized_text(event.notes)

    if "ANULARE COMANDA" in notes:
        return BucketDecision(CanonicalBucket.DELIVERY_REVERSAL, "WME_ANULARE_COMANDA", "Cancellation of order detected")

    if document_type in {"FE", "NIR"} and event.economic_sign == EconomicSign.IN:
        return BucketDecision(CanonicalBucket.RECEIPT, "WME_RECEIPT_DOCUMENT", "Inbound receipt document")

    if document_type == "AE":
        if event.economic_sign == EconomicSign.OUT:
            return BucketDecision(CanonicalBucket.DELIVERY, "WME_AE_DELIVERY", "AE outbound delivery")
        if event.economic_sign == EconomicSign.IN:
            return BucketDecision(CanonicalBucket.RETURN_IN, "WME_AE_RETURN_IN", "AE inbound return")

    if document_type == "BC":
        return BucketDecision(CanonicalBucket.PRODUCTION_CONSUMPTION, "WME_BC_CONSUMPTION", "Production consumption document")

    if document_type == "NP":
        return BucketDecision(CanonicalBucket.FINISHED_GOOD_OUTPUT, "WME_NP_OUTPUT", "Finished good output document")

    if document_type == "NT":
        return BucketDecision(CanonicalBucket.TRANSFER, "WME_NT_TRANSFER", "Transfer document")

    if document_type in {"PV", "COR", "REG"}:
        return BucketDecision(CanonicalBucket.ADJUSTMENT, "WME_ADJUSTMENT_DOCUMENT", "Adjustment or regularization document")

    if event.economic_sign == EconomicSign.IN:
        return BucketDecision(CanonicalBucket.RECEIPT, "WME_POSITIVE_SIGN_RECEIPT", "Positive sign fallback")

    if event.economic_sign == EconomicSign.OUT:
        return BucketDecision(CanonicalBucket.DELIVERY, "WME_NEGATIVE_SIGN_DELIVERY", "Negative sign fallback")

    return BucketDecision(CanonicalBucket.REVIEW, "WME_REVIEW_FALLBACK", "No canonical WME rule matched")


def _normalized_text(value: Any | None) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().upper().split())
